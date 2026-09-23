import html
import json
import os
import re
from pathlib import Path

body = os.environ.get("ISSUE_BODY", "")
match = re.search(r"https://(?:www\.)?instagram\.com/(?:p|reel|reels|tv)/([A-Za-z0-9_-]+)", body, re.I)
if not match:
    raise SystemExit("Instagram 게시물 또는 릴스 주소를 찾지 못했습니다.")

shortcode = match.group(1)
instagram_url = f"https://www.instagram.com/p/{shortcode}/"
# Preserve reel URLs when the supplied text clearly contains /reel/ or /reels/.
if re.search(r"instagram\.com/(?:reel|reels)/" + re.escape(shortcode), body, re.I):
    instagram_url = f"https://www.instagram.com/reel/{shortcode}/"
elif re.search(r"instagram\.com/tv/" + re.escape(shortcode), body, re.I):
    instagram_url = f"https://www.instagram.com/tv/{shortcode}/"

site_base = f"https://hipo020.github.io/instagram-board-embed/posts/{shortcode}/"
out_dir = Path("posts") / shortcode
out_dir.mkdir(parents=True, exist_ok=True)

page = f'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Instagram · {html.escape(shortcode)}</title>
  <link rel="alternate" type="application/json+oembed" href="{site_base}oembed.json" title="Instagram 게시물">
  <style>
    *{{box-sizing:border-box}}
    html,body{{margin:0;min-height:100%;background:#fff}}
    body{{display:grid;justify-items:center;align-items:start;font:16px/1.5 system-ui,sans-serif;overflow-x:hidden}}
    main{{width:100%;max-width:540px;padding:12px;display:flex;flex-direction:column;align-items:center}}
    .instagram-media{{margin:0 auto!important;width:100%!important;min-width:326px!important;max-width:540px!important}}
    iframe.instagram-media{{display:block!important;margin:0 auto!important}}
    a{{color:#5741bf}}
    p{{width:100%;margin:10px 0 0;text-align:center;font-size:13px;color:#555}}
    main:has(iframe) p{{display:none}}
  </style>
</head>
<body>
  <main>
    <blockquote class="instagram-media" data-instgrm-captioned data-instgrm-permalink="{html.escape(instagram_url)}" data-instgrm-version="14">
      <a href="{html.escape(instagram_url)}" target="_blank" rel="noopener noreferrer">Instagram에서 게시물 보기</a>
    </blockquote>
    <p>표시되지 않으면 위 링크로 원본을 열어주세요.</p>
  </main>
  <script async src="https://www.instagram.com/embed.js"></script>
</body>
</html>
'''
(out_dir / "index.html").write_text(page, encoding="utf-8")

oembed = {
    "version": "1.0",
    "type": "rich",
    "title": f"Instagram · {shortcode}",
    "provider_name": "Instagram Reference Viewer",
    "provider_url": site_base,
    "width": 540,
    "height": 720,
    "html": f'<iframe src="{site_base}" width="540" height="720" frameborder="0" allow="autoplay; encrypted-media; fullscreen" allowfullscreen title="Instagram post"></iframe>',
}
(out_dir / "oembed.json").write_text(json.dumps(oembed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
    output.write(f"shortcode={shortcode}\n")
    output.write(f"page_url={site_base}\n")
