#!/usr/bin/env python3
"""TikTok VoC feedback search CLI.

Queries POST https://v.tiktok-row.net/bff/expvoc/voice-list using cookie.txt
in the same directory. Prints a structured summary by default.
"""
import argparse
import base64
import collections
import datetime as dt
import json
import os
import sys
import time
import urllib.request
import urllib.error

API_URL = "https://v.tiktok-row.net/bff/expvoc/voice-list"
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIE_FILE = os.path.join(SKILL_DIR, "cookie.txt")


def load_cookie() -> str:
    if not os.path.exists(COOKIE_FILE):
        sys.exit(f"cookie.txt not found at {COOKIE_FILE}. See SKILL.md to refresh.")
    return open(COOKIE_FILE).read().strip()


def check_cookie_expiry(cookie: str) -> None:
    """Parse the bd_sso_3b6da9 JWT and warn if expiring soon."""
    for part in cookie.split(";"):
        part = part.strip()
        if part.startswith("bd_sso_3b6da9="):
            jwt = part.split("=", 1)[1]
            try:
                payload_b64 = jwt.split(".")[1]
                payload_b64 += "=" * (-len(payload_b64) % 4)
                payload = json.loads(base64.urlsafe_b64decode(payload_b64))
                exp = payload.get("exp", 0)
                remaining = exp - time.time()
                if remaining < 0:
                    sys.stderr.write(f"⚠️  cookie EXPIRED {dt.datetime.fromtimestamp(exp)}. Refresh per SKILL.md.\n")
                elif remaining < 86400:
                    sys.stderr.write(f"⚠️  cookie expires in {remaining/3600:.1f}h ({dt.datetime.fromtimestamp(exp)}). Refresh soon.\n")
            except Exception:
                pass
            return


def call_api(body: dict, cookie: str) -> dict:
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36",
            "Referer": "https://v.tiktok-row.net/feedback-search",
        },
        method="POST",
    )
    last_err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                ct = resp.headers.get("Content-Type", "")
                raw = resp.read().decode("utf-8", errors="replace")
                if "application/json" not in ct:
                    sys.exit(f"Got non-JSON response (Content-Type={ct}). Likely auth issue — refresh cookie. First 300 chars:\n{raw[:300]}")
                return json.loads(raw)
        except urllib.error.HTTPError as e:
            body_text = e.read().decode("utf-8", errors="replace")[:500]
            sys.exit(f"HTTP {e.code}: {body_text}")
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_err = e
            sys.stderr.write(f"  retry {attempt+1}/3 after error: {e}\n")
            time.sleep(2 ** attempt)
    sys.exit(f"All retries failed: {last_err}")


def build_body(args, keyword=None) -> dict:
    """Build voice-list request body using the insights-style Filter (StartTimeMillis/EndTimeMillis/Conditions)."""
    if args.body:
        return json.loads(args.body)
    body: dict = {
        "Keywords": keyword if keyword is not None else args.keywords,
        "Limit": args.limit,
        "Offset": args.offset,
        "SortBy": args.sort_by,
        "SortDesc": not args.no_desc,
    }
    if args.fuzzy:
        body["LangCodesWithDefault"] = True

    conditions: dict = {}
    # Convenience flags
    if args.country:
        conditions["country_code"] = [c.strip().upper() for c in args.country.split(",")]
    if args.idc:
        conditions["idc_code"] = [c.strip().upper() for c in args.idc.split(",")]
    if args.vid:
        conditions["vid_list"] = [v.strip() for v in args.vid.split(",")]
    if args.lang:
        conditions["language"] = [c.strip().upper() for c in args.lang.split(",")]
    # Generic --condition KEY=v1,v2 (repeatable)
    for spec in (args.condition or []):
        if "=" not in spec:
            sys.exit(f"--condition must be KEY=V1[,V2,...] (got {spec!r})")
        k, v = spec.split("=", 1)
        conditions[k.strip()] = [s.strip() for s in v.split(",") if s.strip()]

    filt: dict = {}
    if conditions:
        filt["Conditions"] = conditions
    if args.days is not None:
        end_ms = int(time.time() * 1000)
        start_ms = end_ms - args.days * 86400 * 1000
        filt["StartTimeMillis"] = start_ms
        filt["EndTimeMillis"] = end_ms
    if args.start_ms is not None:
        filt["StartTimeMillis"] = args.start_ms
    if args.end_ms is not None:
        filt["EndTimeMillis"] = args.end_ms

    if filt:
        body["Filter"] = filt
    return body


def load_keywords_file(path: str) -> list:
    """One keyword per line. Skip blanks and lines starting with '#'."""
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def filter_voices(voices: list, args) -> list:
    """Client-side filtering for things the API doesn't natively support."""
    if not args.exclude_country:
        return voices
    excl = {c.strip().upper() for c in args.exclude_country.split(",")}
    return [v for v in voices if (v.get("CountryCode") or "").upper() not in excl]


def print_summary(voices: list, total: str) -> None:
    n = len(voices)
    print(f"\n=== Total matches: {total}  |  Returned: {n} ===\n")

    def topk(field, k=10):
        c = collections.Counter(v.get(field, "") or "(empty)" for v in voices)
        return ", ".join(f"{name}={cnt}" for name, cnt in c.most_common(k))

    print(f"country:   {topk('CountryCode')}")
    print(f"language:  {topk('Languages')}")
    print(f"sentiment: {topk('Sentiment')}")
    print(f"os:        {topk('Os')}")
    print(f"channel:   {topk('SourceChannel')}")
    print(f"L1 label:  {topk('Level1LabelName')}")
    print(f"L2 label:  {topk('Level2LabelName', 15)}")
    print(f"L3 label:  {topk('Level3LabelName', 15)}")
    print(f"ExpL1:     {topk('ExpL1Name')}")
    print(f"ExpL2:     {topk('ExpL2Name', 15)}")
    print(f"ExpL3:     {topk('ExpL3Name', 15)}")
    print(f"BizLine:   {topk('BusinessLine')}")
    if voices:
        times = sorted((v.get("CreateTime", "") or "") for v in voices if v.get("CreateTime"))
        if times:
            print(f"time:      {times[0]} → {times[-1]}")

    print(f"\n=== Voices ({n}) ===")
    for i, v in enumerate(voices, 1):
        c = (v.get("Content", "") or "").replace("\n", " ").replace("<br />", " | ")[:200]
        print(f"[{i:3d}] {(v.get('CreateTime') or '')[:16]} "
              f"{(v.get('CountryCode') or '?'):3s} "
              f"{(v.get('Languages') or '?'):5s} "
              f"{(v.get('Sentiment') or '')[:4]:4s} "
              f"L3={(v.get('Level3LabelName') or '')[:32]:32s} | {c}")


def run_one(keyword: str, args, cookie: str) -> tuple:
    body = build_body(args, keyword=keyword)
    result = call_api(body, cookie)
    if result.get("code") != 0:
        sys.exit(f"API error code={result.get('code')} msg={result.get('msg')} (keyword={keyword!r})")
    data = result.get("data") or {}
    return data.get("Voices") or [], data.get("Total", "?")


def main() -> None:
    p = argparse.ArgumentParser(description="Search TikTok VoC feedback.")
    p.add_argument("keywords", nargs="?", default="", help="search keywords (omit for unfiltered)")
    p.add_argument("--limit", type=int, default=50, help="per-keyword limit (also batch mode)")
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--sort-by", default="create_time")
    p.add_argument("--no-desc", action="store_true", help="ascending instead of descending")
    p.add_argument("--country", help="comma-separated country codes, e.g. US,BR (maps to Conditions.country_code)")
    p.add_argument("--exclude-country", help="comma-separated country codes to drop client-side, e.g. ID,FR (API has no NOT)")
    p.add_argument("--idc", help="idc_code filter, e.g. ROW")
    p.add_argument("--vid", "--experiment-id", dest="vid",
                   help="experiment variant ID (Conditions.vid_list), comma-separated. Filters to users who hit this experiment variant. NOTE: this is the AB-test variant ID, NOT a TikTok video ID.")
    p.add_argument("--condition", action="append",
                   help="generic Conditions filter, KEY=V1[,V2,...]; repeatable. Valid keys: country_code, idc_code, vid_list (experiment variant id), source_channel, os, product_line, business_line, exp_business_line, app_id, app_version, app_info_channel, language, level1_label_id, level2_label_id (others may exist; field-name suffix matters — e.g. vid_list NOT vid).")
    p.add_argument("--lang", help="(legacy, prefer --condition language=EN) comma-separated languages")
    p.add_argument("--days", type=int, help="only last N days")
    p.add_argument("--start-ms", type=int, help="StartTimeMillis (epoch ms)")
    p.add_argument("--end-ms", type=int, help="EndTimeMillis (epoch ms)")
    p.add_argument("--fuzzy", action="store_true",
                   help="multi-language match (LangCodesWithDefault=true). Same as front-end searchMode=fuzzy. Typically ~2x recall.")
    p.add_argument("--keywords-file", help="path to file with one keyword/phrase per line; runs batch + dedupes by VocId")
    p.add_argument("--raw", action="store_true", help="print raw JSON only")
    p.add_argument("--out", help="path to save full JSON response")
    p.add_argument("--body", help="full custom JSON body (overrides other args)")
    args = p.parse_args()

    cookie = load_cookie()
    check_cookie_expiry(cookie)

    # batch mode
    if args.keywords_file:
        kws = load_keywords_file(args.keywords_file)
        sys.stderr.write(f"batch mode: {len(kws)} keywords\n")
        merged: dict = {}
        per_kw_total: dict = {}
        per_kw_hits_after_filter: dict = {}
        for kw in kws:
            voices, total = run_one(kw, args, cookie)
            voices = filter_voices(voices, args)
            per_kw_total[kw] = total
            per_kw_hits_after_filter[kw] = len(voices)
            for v in voices:
                vid = v.get("VocId") or v.get("OriginalId") or id(v)
                if vid not in merged:
                    merged[vid] = (kw, v)
            sys.stderr.write(f"  '{kw}' → total={total}, kept={len(voices)}\n")
        voices_out = [v for _, v in merged.values()]
        voices_out.sort(key=lambda v: v.get("CreateTime") or "", reverse=not args.no_desc)
        out_path = args.out or "/tmp/voc_batch.json"
        with open(out_path, "w") as f:
            json.dump({"per_keyword_total": per_kw_total,
                       "per_keyword_kept": per_kw_hits_after_filter,
                       "dedup_count": len(voices_out),
                       "voices": voices_out,
                       "match_keyword_for_first_seen": {str(vid): kw for vid, (kw, _) in merged.items()}},
                      f, ensure_ascii=False, indent=2)
        sys.stderr.write(f"saved → {out_path}\n")
        print(f"\n=== Batch summary ===")
        for kw, t in per_kw_total.items():
            print(f"  '{kw:<35}' Total={t:<10} kept={per_kw_hits_after_filter[kw]}")
        print(f"\nDeduped union: {len(voices_out)} voices")
        if not args.raw:
            print_summary(voices_out, total=f"dedup={len(voices_out)} from {sum(int(t) if str(t).isdigit() else 0 for t in per_kw_total.values()):,} matches")
        return

    # single-query mode
    body = build_body(args)
    result = call_api(body, cookie)
    if result.get("code") != 0:
        sys.exit(f"API error code={result.get('code')} msg={result.get('msg')}")
    data = result.get("data") or {}
    voices = data.get("Voices") or []
    total = data.get("Total", "?")
    voices = filter_voices(voices, args)

    out_path = args.out or f"/tmp/voc_{(args.keywords or 'all').replace(' ','_')[:40]}.json"
    with open(out_path, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    sys.stderr.write(f"saved full JSON → {out_path}\n")

    if args.raw:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print_summary(voices, total)


if __name__ == "__main__":
    main()
