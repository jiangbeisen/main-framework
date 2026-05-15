#!/usr/bin/env python3
"""TikTok Content Discovery Platform (FCP) popup-list CLI.

Queries POST https://tiktok-cdp-i18n.tiktok-row.net/api/v1/popup/list using
cookie.txt in the same directory. Body {} returns the full list (~280 entries,
~1.2MB JSON) so we pull once and filter client-side.
"""
import argparse
import base64
import collections
import datetime as dt
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

API_URL = "https://tiktok-cdp-i18n.tiktok-row.net/api/v1/popup/list"
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIE_FILE = os.path.join(SKILL_DIR, "cookie.txt")
DEFAULT_CACHE = "/tmp/fcp_popup_list.json"


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
            "fcp-tenant-id": "1",
            "Origin": "https://tiktok-cdp-i18n.tiktok-row.net",
            "Referer": "https://tiktok-cdp-i18n.tiktok-row.net/fcp/resource-bit/popup-window/list",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36",
        },
        method="POST",
    )
    last_err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
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


def fetch_or_cache(cookie: str, cache_path: str, max_age_sec: int, force: bool) -> dict:
    """Reuse cached JSON if fresh; otherwise pull and write cache."""
    if not force and os.path.exists(cache_path):
        age = time.time() - os.path.getmtime(cache_path)
        if age < max_age_sec:
            sys.stderr.write(f"using cache {cache_path} (age {age/60:.1f} min)\n")
            return json.load(open(cache_path))
    sys.stderr.write("calling popup/list ...\n")
    result = call_api({}, cookie)
    if result.get("status_code") not in (0, None):
        # The actual API returns no status_code on success; only check if present.
        msg = result.get("status_msg")
        if msg and msg != "success":
            sys.exit(f"API error: status_code={result.get('status_code')} status_msg={msg}")
    with open(cache_path, "w") as f:
        json.dump(result, f, ensure_ascii=False)
    sys.stderr.write(f"cached → {cache_path}\n")
    return result


# Status codes are inferred from observed values: 0/1/2/3
# We keep the raw int and just label them in summaries.
STATUS_LABELS = {0: "0 草稿/未上线?", 1: "1 启用", 2: "2", 3: "3 下线?"}


def get(p: dict, *path, default=""):
    cur = p
    for k in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
        if cur is None:
            return default
    return cur


def matches(p: dict, args) -> bool:
    ps = p.get("popup_struct") or {}
    if args.biz:
        wanted = {b.strip().lower() for b in args.biz.split(",")}
        if (ps.get("biz_line") or "").lower() not in wanted:
            return False
    if args.status is not None:
        if ps.get("status") not in args.status:
            return False
    if args.creator:
        if args.creator.lower() not in (ps.get("creator") or "").lower():
            return False
    if args.pm:
        if args.pm.lower() not in (ps.get("pm_poc") or "").lower():
            return False
    if args.country:
        wanted = {c.strip().upper() for c in args.country.split(",")}
        countries = ps.get("show_country") or []
        if isinstance(countries, str):
            countries = [countries]
        country_set = {str(c).upper() for c in countries}
        if not (wanted & country_set):
            return False
    if args.search:
        needle = args.search.lower()
        haystack = " ".join(str(ps.get(k) or "") for k in (
            "name", "title", "description", "category_desc", "show_crowd_desc")).lower()
        key = (p.get("popup_statistic") or {}).get("key") or ""
        haystack += " " + key.lower()
        if needle not in haystack:
            return False
    if args.key:
        key = (p.get("popup_statistic") or {}).get("key") or ""
        if args.key.lower() != key.lower():
            return False
    return True


def summary_table(popups: list, total: int) -> None:
    n = len(popups)
    print(f"\n=== Popups: matched {n} / total {total} ===\n")

    def topk(getter, k=15):
        c = collections.Counter()
        for p in popups:
            val = getter(p)
            if isinstance(val, list):
                for v in val:
                    c[str(v) or "(empty)"] += 1
            else:
                c[str(val) if val not in ("", None) else "(empty)"] += 1
        return ", ".join(f"{name}={cnt}" for name, cnt in c.most_common(k))

    g = lambda *p: (lambda d: get(d, *p))
    print(f"biz_line:   {topk(g('popup_struct','biz_line'))}")
    print(f"status:     {topk(lambda p: STATUS_LABELS.get(get(p,'popup_struct','status'), get(p,'popup_struct','status')))}")
    print(f"show_type:  {topk(g('popup_struct','show_type'))}")
    print(f"show_scene: {topk(g('popup_struct','show_scene'), 10)}")
    print(f"creator:    {topk(g('popup_struct','creator'), 10)}")
    print(f"pm_poc:     {topk(g('popup_struct','pm_poc'), 10)}")
    print(f"country:    {topk(g('popup_struct','show_country'), 20)}")
    print()


def list_rows(popups: list, limit: int) -> None:
    print(f"=== Rows (showing {min(limit, len(popups))}) ===")
    for i, p in enumerate(popups[:limit], 1):
        ps = p.get("popup_struct") or {}
        key = (p.get("popup_statistic") or {}).get("key") or ""
        title = (ps.get("title") or ps.get("name") or "")[:50]
        desc = (ps.get("description") or ps.get("category_desc") or "").replace("\n", " ")[:80]
        print(f"[{i:3d}] status={ps.get('status')} "
              f"biz={ps.get('biz_line') or '?':<22.22} "
              f"key={key:<40.40} | {title} | {desc}")


def print_detail(p: dict) -> None:
    ps = p.get("popup_struct") or {}
    stat = p.get("popup_statistic") or {}
    rd = p.get("rule_decision") or {}
    print(f"key:           {stat.get('key')}")
    print(f"name:          {ps.get('name')}")
    print(f"title:         {ps.get('title')}")
    print(f"biz_line:      {ps.get('biz_line')}")
    print(f"status:        {STATUS_LABELS.get(ps.get('status'), ps.get('status'))}")
    print(f"show_type:     {ps.get('show_type')}")
    print(f"show_scene:    {ps.get('show_scene')}")
    print(f"show_country:  {ps.get('show_country')}")
    print(f"show_condition:{ps.get('show_condition')}")
    print(f"creator:       {ps.get('creator')}")
    print(f"pm_poc:        {ps.get('pm_poc')}")
    print(f"rd_poc:        {ps.get('rd_poc')}")
    print(f"qa_poc:        {ps.get('qa_poc')}")
    print(f"category:      {ps.get('category')}  ({ps.get('category_desc')})")
    print(f"description:   {(ps.get('description') or '')[:300]}")
    print(f"prd_doc:       {ps.get('prd_doc')}")
    print(f"meego_link:    {ps.get('meego_link')}")
    print(f"diagram_url:   {ps.get('diagram_url')}")
    print(f"ctr:           {stat.get('ctr')}")
    print(f"shrink_image:  {(ps.get('shrink_image') or {}).get('shrink_240', '')[:120]}...")
    print(f"--- rule_decision keys ({len(rd)}): {', '.join(list(rd.keys())[:10])}{'...' if len(rd)>10 else ''}")


def download_thumbs(popups: list, n: int, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    sys.stderr.write(f"downloading up to {n} thumbnails into {out_dir}\n")
    for i, p in enumerate(popups[:n], 1):
        ps = p.get("popup_struct") or {}
        si = ps.get("shrink_image") or {}
        url = si.get("shrink_240") or si.get("shrink_480") or si.get("shrink_720")
        if not url:
            sys.stderr.write(f"  #{i} no image\n")
            continue
        key = (p.get("popup_statistic") or {}).get("key") or f"item{i}"
        safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in key)[:60]
        tmp = os.path.join(out_dir, f"{i:03d}_{safe}.image")
        try:
            urllib.request.urlretrieve(url, tmp)
            with open(tmp, "rb") as f:
                head = f.read(8)
            ext = "png" if head.startswith(b"\x89PNG") else ("jpg" if head[:3] == b"\xff\xd8\xff" else ("webp" if head[:4] == b"RIFF" else "bin"))
            final = tmp[:-6] + "." + ext
            os.rename(tmp, final)
            print(f"  {final}")
        except Exception as e:
            sys.stderr.write(f"  #{i} {key} FAILED: {e}\n")


def main() -> None:
    p = argparse.ArgumentParser(description="Query TikTok FCP popup-window list.")
    p.add_argument("--biz", help="comma-separated biz_line filter, e.g. 'Social,Feeds' (case-insensitive)")
    p.add_argument("--status", type=lambda s: [int(x) for x in s.split(",")],
                   help="status codes, comma-separated, e.g. '1' or '0,1'")
    p.add_argument("--creator", help="substring match against creator field")
    p.add_argument("--pm", help="substring match against pm_poc")
    p.add_argument("--country", help="comma-separated countries; matches if popup's show_country intersects (case-insensitive)")
    p.add_argument("--search", help="substring search across name/title/description/category_desc/key (case-insensitive)")
    p.add_argument("--key", help="exact popup key match")
    p.add_argument("--limit", type=int, default=30, help="max rows to print (default 30)")
    p.add_argument("--detail", help="print full details for a single popup by key")
    p.add_argument("--thumbs", type=int, metavar="N",
                   help="also download first N thumbnails of the filtered set to /tmp/fcp_thumbs/")
    p.add_argument("--thumbs-dir", default="/tmp/fcp_thumbs", help="thumbnail output dir")
    p.add_argument("--raw", action="store_true", help="print filtered records as raw JSON (full popup_struct)")
    p.add_argument("--out", help="save filtered records to this JSON path")
    p.add_argument("--refresh", action="store_true", help="bypass cache, refetch from API")
    p.add_argument("--cache-min", type=int, default=15, help="cache TTL in minutes (default 15)")
    p.add_argument("--cache-path", default=DEFAULT_CACHE)
    args = p.parse_args()

    cookie = load_cookie()
    check_cookie_expiry(cookie)
    result = fetch_or_cache(cookie, args.cache_path, args.cache_min * 60, args.refresh)
    popups_all = result.get("popups") or []
    total = len(popups_all)

    # --detail short-circuit
    if args.detail:
        args.key = args.detail
        filtered = [p for p in popups_all if matches(p, args)]
        if not filtered:
            sys.exit(f"no popup with key={args.detail!r}")
        print_detail(filtered[0])
        if args.thumbs:
            download_thumbs(filtered, args.thumbs, args.thumbs_dir)
        return

    filtered = [p for p in popups_all if matches(p, args)]

    if args.out:
        with open(args.out, "w") as f:
            json.dump(filtered, f, ensure_ascii=False, indent=2)
        sys.stderr.write(f"saved filtered → {args.out}\n")

    if args.raw:
        print(json.dumps(filtered, ensure_ascii=False, indent=2))
        return

    summary_table(filtered, total)
    list_rows(filtered, args.limit)

    if args.thumbs:
        download_thumbs(filtered, args.thumbs, args.thumbs_dir)


if __name__ == "__main__":
    main()
