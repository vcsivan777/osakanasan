import os
from datetime import datetime
from curl_cffi import requests
from bs4 import BeautifulSoup

# Top.ggのトレンドページ
url = "https://top.gg"

print("Top.ggからデータと紹介文を取得中（ロゴ＆バナー搭載版）...")

try:
    response = requests.get(url, impersonate="chrome")
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    bot_links = soup.select("a[href^='/bot/']")
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 💡 サイト最上部にグラデーションバナーとロゴを埋め込むCSS/HTML
    markdown_content = f"""<style>
    body {{ background-color: #0b0f19 !important; color: #f5f5f5 !important; font-family: -apple-system, BlinkMacSystemFont, sans-serif; padding: 0; margin: 0; }}
    
    /* 🌟 近未来風サイバーバナーのデザイン */
    .hero-banner {{
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border-bottom: 2px solid #3b82f6;
        padding: 60px 24px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }}
    .hero-banner::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.1) 0%, transparent 80%);
    }}
    
    /* 🌟 サイトのオリジナルロゴ */
    .site-logo {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(45deg, #3b82f6, #8b5cf6);
        color: white;
        padding: 12px 24px;
        border-radius: 50px;
        font-weight: 900;
        font-size: 1.5rem;
        letter-spacing: 2px;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.2);
    }}
    .site-logo span {{ margin-right: 8px; font-size: 1.8rem; }}
    
    .site-title {{ font-size: 2.2rem; font-weight: 800; color: #ffffff; margin: 0 0 12px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }}
    .site-subtitle {{ color: #94a3b8; font-size: 1rem; max-width: 600px; margin: 0 auto 16px auto; line-height: 1.6; }}
    .update-badge {{ display: inline-block; background-color: #1e293b; border: 1px solid #475569; color: #38bdf8; font-size: 0.8rem; padding: 6px 16px; border-radius: 20px; font-weight: 600; }}

    /* メインコンテンツ（グリッド） */
    .main-content {{ max-width: 1200px; margin: 0 auto; padding: 40px 24px; }}
    .grid-container {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 24px; }}
    
    /* カードの微調整 */
    .bot-card {{ display: block; background-color: #111827; border: 1px solid #1f2937; border-radius: 16px; padding: 24px; text-decoration: none !important; color: #ffffff !important; transition: all 0.25s ease-in-out; }}
    .bot-card:hover {{ background-color: #1f2937; border-color: #3b82f6; transform: translateY(-6px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 0 15px rgba(59, 130, 246, 0.2); }}
    .bot-header {{ display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }}
    .bot-icon {{ font-size: 1.4rem; background-color: #1f2937; padding: 6px; border-radius: 10px; }}
    .bot-name {{ font-size: 1.2rem; font-weight: bold; color: #ffffff !important; }}
    .bot-desc {{ color: #94a3b8; font-size: 0.9rem; margin: 0 0 16px 0; line-height: 1.6; height: 3.2em; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }}
    .bot-link-text {{ text-align: right; font-size: 0.85rem; color: #3b82f6; font-weight: 600; transition: color 0.2s; }}
    .bot-card:hover .bot-link-text {{ color: #60a5fa; }}
</style>

<!-- 🌟 最上部のオリジナルヘッダーバナーエリア -->
<div class="hero-banner">
    <!-- あなただけのオリジナルロゴ -->
    <div class="site-logo">
        <span>🐟</span>OSAKANA BOT TRENDS
    </div>
    <h1 class="site-title">海外Discord Botトレンドランキング</h1>
    <p class="site-subtitle">世界最大のBotサイトから、今まさに海外で大流行している大注目のDiscord Botを24時間自動集約。あなたのサーバーを最強に拡張しましょう！</p>
    <div class="update-badge">⚡ 最終自動更新: {today_str}</div>
</div>

<div class="main-content">
    <div class="grid-container">
"""

    count = 0
    seen_urls = set()

    for link in bot_links:
        bot_url = "https://top.gg" + link.get("href")
        if bot_url in seen_urls or "/vote" in bot_url:
            continue

        bot_name = link.get_text(strip=True)
        if "Vote" in bot_name:
            bot_name = bot_name.replace("Vote", "").strip(" ()")
        if not bot_name:
            continue
            
        seen_urls.add(bot_url)

        bot_desc = ""
        parent = link.find_parent()
        for _ in range(3):
            if parent:
                for text_el in parent.find_all(['p', 'div', 'span']):
                    t = text_el.get_text(strip=True)
                    if t and 10 < len(t) < 150 and bot_name not in t and "Vote" not in t:
                        bot_desc = t
                        break
            if bot_desc:
                break
            if parent:
                parent = parent.find_parent()

        if not bot_desc:
            bot_desc = f"{bot_name} is a trending Discord bot on Top.gg. Click to view full details and features."

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

    markdown_content += "\n</div></div>"

    if count > 0:
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"成功！ バナー付きの『index.html』を保存しました。")
    else:
        print("Botが見つかりませんでした。")

except Exception as e:
    print(f"エラーが発生しました: {e}")
