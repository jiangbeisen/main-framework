#!/usr/bin/env python3
"""
Stage 4: 把命中行的截图嵌入 L 列。
Usage: python3 embed_images.py YYYY-MM-DD

注意：lark-cli +write-image 强制相对路径，所以脚本会 cd 到 resized 目录，
然后调用 --image './<filename>'.
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
    verdicts = [json.loads(l) for l in open(os.path.join(workdir, "verdicts.jsonl")) if l.strip()]
    hits = [v for v in verdicts if v.get("is_fyp") and v.get("has_popup")]
    resized_dir = os.path.join(workdir, "resized")
    os.chdir(resized_dir)
    success = 0
    for i, v in enumerate(hits):
        row = i + 2  # row 1 is header
        fname = f"{v['voc_id']}_{v['idx']}.jpg"
        if not os.path.exists(fname):
            print(f"  row {row}: missing {fname}, skip")
            continue
        r = subprocess.run([
            "lark-cli", "sheets", "+write-image",
            "--url", sheet["url"], "--sheet-id", sheet["sheet_id"],
            "--range", f"L{row}", "--image", f"./{fname}",
        ], capture_output=True, text=True)
        try:
            ok = json.loads(r.stdout).get("ok")
        except Exception:
            ok = False
        print(f"  row {row}: {fname} → {'OK' if ok else 'FAIL '+r.stdout[:200]}")
        if ok:
            success += 1
    print(f"\nembedded {success}/{len(hits)} images")


if __name__ == "__main__":
    main()
