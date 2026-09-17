import os
from datetime import datetime
from curl_cffi import requests
from bs4 import BeautifulSoup

# Top.ggのトレンドページ
url = "https://top.gg"

print("Top.ggからデータと紹介文を取得中...")

try:
    response = requests.get(url, impersonate="chrome")
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    bot_links = soup.select("a[href^='/bot/']")
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # CSSデザインとHTMLテンプレートの構築部分
    markdown_content = f"""<style>
    body {{ background-color: #171717 !important; color: #f5f5f5 !important; font-family: -apple-system, BlinkMacSystemFont, sans-serif; padding: 24px; }}
    .grid-container {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 30px; }}
    .bot-card {{ display: block; background-color: #262626; border: 1px solid #404040; border-radius: 12px; padding: 20px; text-decoration: none !important; color: #ffffff !important; transition: all 0.2s ease-in-out; }}
    .bot-card:hover {{ background-color: #404040; border-color: #737373; transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); }}
    .bot-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }}
    .bot-icon {{ font-size: 1.3rem; }}
    .bot-name {{ font-size: 1.2rem; font-weight: bold; color: #ffffff !important; }}
    .bot-desc {{ color: #a3a3a3; font-size: 0.9rem; margin: 0 0 12px 0; line-height: 1.5; height: 2.7em; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }}
    .bot-link-text {{ text-align: right; font-size: 0.8rem; color: #a3a3a3; }}
    .bot-card:hover .bot-link-text {{ color: #ffffff; }}
</style>

# 海外で今大流行中のDiscord Botトレンドランキング

最終更新日時: {today_str} (自動更新)

世界最大のBotサイト「Top.gg」でトレンドに入っている大注目のDiscord Botを集約しています。

---

<div class="grid-container">
"""

    count = 0
    seen_urls = set()

    for link in bot_links:
        bot_url = "https://top.gg" + link.get("href")
        if bot_url in seen_urls:
            continue
        seen_urls.add(bot_url)

        bot_name = link.get_text(strip=True)
        if "Vote" in bot_name:
            bot_name = bot_name.replace("Vote", "").strip(" ()")
        if not bot_name:
            continue

        bot_desc = "今Top.ggのトレンドにランクインしている注目のBotです。"
        parent = link.find_parent()
        if parent:
            desc_element = parent.select_one("p") or parent.find_next("p")
            if desc_element:
                text = desc_element.get_text(strip=True)
                if text and len(text) > 5 and text != bot_name:
                    bot_desc = text

        if len(bot_name) > 1:
            count += 1
            markdown_content += f"""
<a href="{bot_url}" class="bot-card" target="_blank">
    <div class="bot-header">
        <span class="bot-icon">🤖</span>
        <span class="bot-name">{count}. {bot_name}</span>
    </div>
    <p class="bot-desc">{bot_desc}</p>
    <div class="bot-link-text">詳細を見る ➔</div>
</a>"""
            if count >= 20:
                break

    markdown_content += "\n</div>"

    if count > 0:
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"成功！ {count}件のBotデータを『index.html』に保存しました。")
    else:
        print("Botが見つかりませんでした。")

except Exception as e:
    print(f"エラーが発生しました: {e}")
