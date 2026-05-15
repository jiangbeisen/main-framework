#!/usr/bin/env python3
"""
Stage 3: 读 verdicts.jsonl + rows.json，把"上次写入之后新增的 hits"append 到表。
Usage: python3 append_hits.py YYYY-MM-DD
verdicts.jsonl 每行：{"voc_id":..,"idx":..,"is_fyp":bool,"has_popup":bool,"popup_type":str,"note":str}
"""
import datetime, json, os, subprocess, sys


def main():
    if len(sys.argv) < 2:
        date_str = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        date_str = sys.argv[1]
    workdir = f"/tmp/popup_{date_str}"
    rows = {(r["voc_id"], r["idx"]): r for r in json.load(open(os.path.join(workdir, "rows.json")))}
    sheet = json.load(open(os.path.join(workdir, "sheet.json")))
    verdicts_path = os.path.join(workdir, "verdicts.jsonl")
    marker = os.path.join(workdir, "written_count.txt")

    verdicts = [json.loads(l) for l in open(verdicts_path) if l.strip()]
    hits = [v for v in verdicts if v.get("is_fyp") and v.get("has_popup")]
    written = int(open(marker).read().strip()) if os.path.exists(marker) else 0
    new_hits = hits[written:]
    print(f"total hits so far: {len(hits)}, new to append: {len(new_hits)}")
    if not new_hits:
        return
    payload = []
    for v in new_hits:
        key = (v["voc_id"], v["idx"])
        if key not in rows:
            continue
        r = rows[key]
        payload.append([
            r["voc_id"], r["create_time"], r["country"], r["lang"],
            r["content"][:300],
            {"type": "url", "text": f"图片 {r['idx']}", "link": r["url"]},
            r["resized"],
            "是" if v["is_fyp"] else "否",
            "是" if v["has_popup"] else "否",
            v.get("popup_type", ""),
            v.get("note", ""),
        ])
    r = subprocess.run([
        "lark-cli", "sheets", "+append",
        "--url", sheet["url"], "--sheet-id", sheet["sheet_id"],
        "--values", json.dumps(payload, ensure_ascii=False),
        "-q", ".data.updates",
    ], capture_output=True, text=True)
    print(r.stdout.strip()[:500])
    if r.returncode != 0 or '"ok"' in r.stdout and '"ok": false' in r.stdout:
        print("ERR:", r.stderr, file=sys.stderr)
        sys.exit(1)
    open(marker, "w").write(str(len(hits)))


if __name__ == "__main__":
    main()
