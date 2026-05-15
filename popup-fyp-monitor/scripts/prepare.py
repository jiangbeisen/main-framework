#!/usr/bin/env python3
"""
Stage 1: 拉取 + 过滤 + 下载 + 缩放。
Usage: python3 prepare.py YYYY-MM-DD
输出：
  /tmp/popup_<date>/manifest.json   每张图一条 {voc_id, idx, url, local, resized, skipped}
  /tmp/popup_<date>/rows.json       每张图的反馈元数据（VocId/CreateTime/Country/Lang/Content）
"""
import datetime, json, os, subprocess, sys, urllib.request

FEEDBACK_DIR = os.path.expanduser("~/work/skills/feedback")
FEEDBACK_PY = os.path.join(FEEDBACK_DIR, "feedback.py")
COOKIE_PATH = os.path.join(FEEDBACK_DIR, "cookie.txt")
KEYWORD = "pop up"


def day_ms_range(date_str: str):
    d = datetime.datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
    start = int(d.timestamp() * 1000)
    end = int((d + datetime.timedelta(days=1)).timestamp() * 1000) - 1
    return start, end


def fetch_all(start_ms: int, end_ms: int, workdir: str):
    """分页拉取所有 voices。每页 50，最多 3 次重试。"""
    voices = []
    for offset in range(0, 2000, 50):
        out = os.path.join(workdir, f"_page_{offset}.json")
        cmd = ["python3", FEEDBACK_PY, KEYWORD,
               "--start-ms", str(start_ms), "--end-ms", str(end_ms),
               "--limit", "50", "--offset", str(offset),
               "--out", out, "--raw"]
        for attempt in range(3):
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
                if r.returncode == 0:
                    break
            except subprocess.TimeoutExpired:
                pass
            print(f"  offset={offset} retry {attempt+1}", flush=True)
        page = json.load(open(out))
        page_voices = page.get("data", {}).get("Voices") or []
        print(f"  offset={offset}: got {len(page_voices)}", flush=True)
        voices.extend(page_voices)
        if len(page_voices) < 50:
            break
    # dedupe by VocId
    seen, uniq = set(), []
    for v in voices:
        vid = v.get("VocId")
        if vid in seen:
            continue
        seen.add(vid)
        uniq.append(v)
    return uniq


def download_image(url: str, dst: str, cookie: str) -> bool:
    if os.path.exists(dst) and os.path.getsize(dst) > 1000:
        return True
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Cookie": cookie,
            "Referer": "https://v.tiktok-row.net/",
        })
        with urllib.request.urlopen(req, timeout=30) as r:
            open(dst, "wb").write(r.read())
        return True
    except Exception as e:
        print(f"  download FAIL: {e}", flush=True)
        return False


def resize(src: str, dst: str, max_px: int = 1800):
    if os.path.exists(dst):
        return True
    r = subprocess.run(["sips", "-Z", str(max_px), src, "--out", dst], capture_output=True)
    return r.returncode == 0


def main():
    if len(sys.argv) < 2:
        date_str = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        date_str = sys.argv[1]
    start_ms, end_ms = day_ms_range(date_str)
    workdir = f"/tmp/popup_{date_str}"
    raw_dir = os.path.join(workdir, "raw")
    resized_dir = os.path.join(workdir, "resized")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(resized_dir, exist_ok=True)

    print(f"[1/4] fetch voices for {date_str} ({start_ms}..{end_ms})", flush=True)
    voices = fetch_all(start_ms, end_ms, workdir)
    print(f"  total unique voices: {len(voices)}", flush=True)

    print("[2/4] filter IfHasAttachment==1", flush=True)
    with_att = [v for v in voices if v.get("IfHasAttachment") == "1"]
    print(f"  with attachment: {len(with_att)}", flush=True)

    print("[3/4] download images", flush=True)
    cookie = open(COOKIE_PATH).read().strip()
    manifest, rows = [], []
    fail = 0
    for v in with_att:
        voc = v["VocId"]
        atts = v.get("AttachmentList") or []
        img_atts = [a for a in atts if a.get("FileType2") == "image"]
        content = (v.get("Content") or "").replace("\n", " ").strip()[:500]
        for j, a in enumerate(img_atts):
            url = a.get("Url") or a.get("Uri2")
            if not url:
                continue
            local = os.path.join(raw_dir, f"{voc}_{j}.jpg")
            if not download_image(url, local, cookie):
                fail += 1
                continue
            resized = os.path.join(resized_dir, f"{voc}_{j}.jpg")
            if not resize(local, resized):
                continue
            manifest.append({"voc_id": voc, "idx": j, "url": url,
                             "local": local, "resized": resized, "skipped": False})
            rows.append({"voc_id": voc, "idx": j,
                         "create_time": v.get("CreateTime"),
                         "country": v.get("CountryCode"),
                         "lang": v.get("Languages"),
                         "content": content,
                         "url": url,
                         "resized": resized})
    print(f"  downloaded: {len(manifest)}  failed: {fail}", flush=True)

    print("[4/4] write manifest + rows", flush=True)
    json.dump(manifest, open(os.path.join(workdir, "manifest.json"), "w"), indent=2)
    json.dump(rows, open(os.path.join(workdir, "rows.json"), "w"), ensure_ascii=False, indent=2)
    open(os.path.join(workdir, "verdicts.jsonl"), "a").close()
    open(os.path.join(workdir, "written_count.txt"), "w").write("0")
    print(f"OK → {workdir}", flush=True)
    print(json.dumps({"date": date_str, "workdir": workdir,
                      "voices_total": len(voices),
                      "with_attachment": len(with_att),
                      "images_ready": len(manifest)}))


if __name__ == "__main__":
    main()
