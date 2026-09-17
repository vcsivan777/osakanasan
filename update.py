import os
from datetime import datetime
from curl_cffi import requests
from bs4 import BeautifulSoup

# Top.ggのトレンドページ
url = "https://top.gg"

print("Top.ggからデータを取得中...（グリッドデザイン用HTML埋め込み）")

try:
    # 本物のブラウザのふりをしてアクセス
    response = requests.get(url, impersonate="chrome")
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    bot_links = soup.select("a[href^='/bot/']")

    # 今日の日付を取得
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # --- 1. 灰色モード＋グリッド用のCSSデザインを最初に埋め込む ---
    markdown_content = f"""<style>
    body {{ background-color: #171717 !important; color: #f5f5f5 !important; font-family: -apple-system, BlinkMacSystemFont, sans-serif; padding: 24px; }}
    .grid-container {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; margin-top: 30px; }}
    .bot-card {{ display: block; background-color: #262626; border: 1px solid #404040; border-radius: 12px; padding: 20px; text-decoration: none !important; color: #ffffff !important; transition: all 0.2s ease-in-out; }}
    .bot-card:hover {{ background-color: #404040; border-color: #737373; transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); }}
    .bot-header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }}
    .bot-icon {{ font-size: 1.3rem; }}
    .bot-name {{ font-size: 1.2rem; font-weight: bold; color: #ffffff !important; }}
    .bot-desc {{ color: #a3a3a3; font-size: 0.9rem; margin: 0 0 12px 0; line-height: 1.5; }}
    .bot-link-text {{ text-align: right; font-size: 0.8rem; color: #a3a3a3; }}
    .bot-card:hover .bot-link-text {{ color: #ffffff; }}
</style>

# 海外で今大流行中のDiscord Botトレンドランキング

最終更新日時: {today_str} (自動更新)

世界最大のBotサイト「Top.gg」で、今まさにトレンドに入っている大注目のDiscord Botを自動で集約して紹介しています。あなたのサーバーの機能拡張にぜひ役立ててください！

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

        # 「Vote (142)」などの余計な文字を消してキレイにする処理
        if "Vote" in bot_name:
            bot_name = bot_name.replace("Vote", "").strip(" ()")
        if not bot_name or bot_name == "":
            bot_name = "注目のDiscord Bot"

        if bot_name and len(bot_name) > 1:
            count += 1
            
            # --- 2. ボタン型のHTMLカードをループで追加していく ---
            markdown_content += f"""
<a href="{bot_url}" class="bot-card" target="_blank">
    <div class="bot-header">
        <span class="bot-icon">🤖</span>
        <span class="bot-name">{count}. {bot_name}</span>
    </div>
    <p class="bot-desc">今Top.ggのトレンドにランクインしている注目のBotです。</p>
    <div class="bot-link-text">詳細を見る ➔</div>
</a>"""
            
            # 最大20件まで引っこ抜く
            if count >= 20:
                break

    # --- 3. グリッドの閉じタグを追加 ---
    markdown_content += "\n</div>"

    if count > 0:
        # 集めたデータを「index.md」という名前のファイルとして保存
        with open("index.md", "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"成功！ {count}件のBotデータをグリッドデザインで『index.md』に保存しました。")
    else:
        print("Botが見つかりませんでした。")

except Exception as e:
    print(f"エラーが発生しました: {e}")


        print("Botが見つかりませんでした。")

except Exception as e:
    print(f"エラーが発生しました: {e}")
