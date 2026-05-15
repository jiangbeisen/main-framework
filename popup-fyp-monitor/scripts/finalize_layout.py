#!/usr/bin/env python3
"""
Stage 5: 调整 L 列宽与命中行高，方便看截图。
Usage: python3 finalize_layout.py YYYY-MM-DD
"""
import datetime, json, os, subprocess, sys


def main():
    if len(sys.argv) < 2:
        date_str = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        date_str = sys.argv[1]
    workdir = f"/tmp/popup_{date_str}"
    sheet = json.load(open(os.path.join(workdir, "sheet.json")))
    verdicts = [json.loads(l) for l in open(os.path.join(workdir, "verdicts.jsonl")) if l.strip()]
    hits = [v for v in verdicts if v.get("is_fyp") and v.get("has_popup")]
    n = len(hits)
    if n == 0:
        print("no hits to layout")
        return

    # Rows 2..n+1 → height 400px
    subprocess.run([
        "lark-cli", "sheets", "+update-dimension",
        "--url", sheet["url"], "--sheet-id", sheet["sheet_id"],
        "--dimension", "ROWS", "--start-index", "2", "--end-index", str(n + 1),
        "--fixed-size", "400",
    ], check=False)
    # Column L (index 12) → width 220px
    subprocess.run([
        "lark-cli", "sheets", "+update-dimension",
        "--url", sheet["url"], "--sheet-id", sheet["sheet_id"],
        "--dimension", "COLUMNS", "--start-index", "12", "--end-index", "12",
        "--fixed-size", "220",
    ], check=False)
    print(f"layout adjusted: {n} rows @ 400px, col L @ 220px")
    print(f"URL: {sheet['url']}")


if __name__ == "__main__":
    main()
