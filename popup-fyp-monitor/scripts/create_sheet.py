#!/usr/bin/env python3
"""
Stage 2: 创建飞书电子表格并写入表头。
Usage: python3 create_sheet.py YYYY-MM-DD
输出：/tmp/popup_<date>/sheet.json  {token, sheet_id, url}
"""
import datetime, json, os, subprocess, sys

HEADERS = ["VocId", "CreateTime", "Country", "Language", "Content",
           "截图URL", "本地路径", "是否FYP", "是否弹窗容器",
           "弹窗类型", "识别说明", "截图"]


def main():
    if len(sys.argv) < 2:
        date_str = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        date_str = sys.argv[1]
    workdir = f"/tmp/popup_{date_str}"
    sheet_file = os.path.join(workdir, "sheet.json")
    if os.path.exists(sheet_file):
        print(f"sheet.json exists, reuse: {open(sheet_file).read()}")
        return
    title = f"VoC pop up {date_str} - FYP 弹窗截图筛选"
    r = subprocess.run([
        "lark-cli", "sheets", "+create", "--title", title,
        "--headers", json.dumps(HEADERS, ensure_ascii=False),
    ], capture_output=True, text=True)
    if r.returncode != 0:
        print("ERR:", r.stderr or r.stdout, file=sys.stderr)
        sys.exit(1)
    create_out = json.loads(r.stdout)
    if not create_out.get("ok"):
        print("ERR:", json.dumps(create_out), file=sys.stderr)
        sys.exit(1)
    token = create_out["data"]["spreadsheet_token"]
    url = create_out["data"]["url"]
    # info → sheet_id
    info = subprocess.run([
        "lark-cli", "sheets", "+info", "--url", url, "-q", ".data.sheets.sheets[0].sheet_id"
    ], capture_output=True, text=True)
    sheet_id = info.stdout.strip().strip('"')
    out = {"token": token, "sheet_id": sheet_id, "url": url, "title": title}
    json.dump(out, open(sheet_file, "w"), indent=2)
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
