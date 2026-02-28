#!/usr/bin/env python3
import json, urllib.request, os, time
from urllib.parse import urlparse, quote

DATA_DIR = '/root/wangziyu-api/data'
LYRICS_DIR = os.path.join(DATA_DIR, 'lyrics')
os.makedirs(LYRICS_DIR, exist_ok=True)

with open(os.path.join(DATA_DIR, 'music.json'), encoding='utf-8') as f:
    music = json.load(f)

success = 0
failed = []
for m in music:
    lyric = m.get('lyric', '')
    if not lyric or not lyric.startswith('http'):
        continue
    # 用歌曲 id 作为文件名，避免中文路径问题
    local_path = os.path.join(LYRICS_DIR, f"{m['id']}.lrc")
    if os.path.exists(local_path):
        success += 1
        continue
    try:
        parsed = urlparse(lyric)
        safe_path = quote(parsed.path, safe='/%')
        encoded_url = f"{parsed.scheme}://{parsed.netloc}{safe_path}"
        req = urllib.request.Request(encoded_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='replace')
        with open(local_path, 'w', encoding='utf-8') as f:
            f.write(content)
        success += 1
        print(f"  ✅ {m['name']}")
    except Exception as e:
        failed.append(m['name'])
        print(f"  ❌ {m['name']}: {e}")

print(f"\n完成: {success} 成功, {len(failed)} 失败")
if failed:
    print("失败列表:", failed)
