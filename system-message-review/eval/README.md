# 系统消息审核 Eval

## 目的

用历史审批案例系统性评测 AI 审批质量，定向调优 SKILL.md 和 references。

## 评测流程

1. **准备案例**：从历史审批表中提取，按 `cases/` 目录下的 JSONL 格式整理
2. **跑评测**：对每条案例用 skill 审核，记录 AI 结论和依据
3. **对比打分**：与人工结论对比，标记一致/不一致
4. **错误分析**：对不一致案例分类错误类型
5. **调优**：针对高频错误类型修改 skill → 重新跑 eval → 确认改进无回归

## 案例格式

每条案例一行 JSON，字段如下：

```json
{
  "id": "40520578",
  "difficulty": "simple|boundary|controversial",
  "category_tag": "compliance|activity|finance|feature_promo|subscription|rule_change",
  "input": {
    "template_name": "smb_kyb_upgrade_rba_tc",
    "channel": "LIVE",
    "category": "Activities",
    "title": "Upgrade to a verified Business Account",
    "content": "You've successfully verified your business. Now, finish the setup to unlock the TikTok Business Suite and advanced lead generation tools.",
    "send_reason": "notify the target recipients about the benefit of complete RBA verification",
    "target_audience": "existing SMB creators who are KYB verified and have not completed RBA process",
    "trigger_logic": "one time sending for existing smb KYB creators who have not completed the RBA registration",
    "estimated_users": 98300,
    "new_user_receive": false,
    "frequency_control": false,
    "is_must_reach": false,
    "is_priority": false
  },
  "expected": {
    "conclusion": "reject",
    "reasoning": "主信息是引导完成设置以解锁功能，属于功能推广/活动引流，不是结果通知",
    "key_rules": ["5.1-功能推广", "6.3-主信息倾向拒绝"]
  }
}
```

## 案例文件

| 文件 | 内容 | 目标数量 |
|------|------|---------|
| pass-simple.jsonl | 明显通过（合规/安全/交易/举报结果等） | 10-15 条 |
| reject-simple.jsonl | 明显拒绝（纯营销/功能推广/活动引流等） | 10-15 条 |
| boundary.jsonl | 边界案例（活动类/金融类/订阅类/经营权益类） | 15-20 条 |
| regression.jsonl | 历史误判案例（AI 与人工不一致的） | 全部收录 |

## 评测指标

| 指标 | 公式 | 目标 |
|------|------|------|
| 整体准确率 | 一致数 / 总数 | >90% |
| 简单案例准确率 | 简单案例一致数 / 简单案例总数 | >95% |
| 拒绝召回率 | 正确拒绝数 / 应拒绝总数 | >95%（漏放代价最高） |
| 通过精确率 | 正确通过数 / AI判通过总数 | >90% |
| 规则命中率 | 依据命中正确规则的比例 | >85% |

## 错误分类

对每条不一致案例，标记错误类型：

| 类型 | 含义 | 调优方向 |
|------|------|---------|
| false_pass（漏放） | 人工拒绝但 AI 通过 | 加强拒绝口径 |
| false_reject（误杀） | 人工通过但 AI 拒绝 | 放宽通过口径或补充边界规则 |
| wrong_reasoning | 结论一致但依据引用错误 | 修正规则表述 |
| missed_precheck | 未检查前置项 | 强化前置校验 |

## 调优循环

```
eval 结果 → 按错误类型聚类 → 定位 skill/rubric 中的问题 → 修改 → 重新跑 eval → 确认改进无回归
```

重点关注：
- false_pass 最优先修（放过了不该放的）
- 边界案例的 false_reject 次优先（过度保守会影响业务效率）
- wrong_reasoning 最后修（结论对但依据不精准）
