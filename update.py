import os
from datetime import datetime
from curl_cffi import requests
from bs4 import BeautifulSoup

# Top.ggのトレンドページ
url = "https://top.gg"

print("Top.ggからデータを取得中...（ファイル書き出し中）")

try:
    # 本物のブラウザのふりをしてアクセス
    response = requests.get(url, impersonate="chrome")
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    bot_links = soup.select("a[href^='/bot/']")

    # 今日の日付を取得（サイトに掲載するため）
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # --- ここからWEBサイト用のファイル（Markdown）の中身を作成 ---
    markdown_content = f"""# 海外で今大流行中のDiscord Botトレンドランキング

最終更新日時: {today_str} (自動更新)

世界最大のBotサイト「Top.gg」で、今まさにトレンドに入っている大注目のDiscord Botを自動で集約して紹介しています。あなたのサーバーの機能拡張にぜひ役立ててください！

---

"""

    count = 0
    seen_urls = set()

    for link in bot_links:
        bot_url = "https://top.gg" + link.get("href")
        
        if bot_url in seen_urls:
            continue
        seen_urls.add(bot_url)

        bot_name = link.get_text(strip=True)

        if bot_name and len(bot_name) > 1:
            count += 1
            # 記事に載せる用の文章を組み立てる
            markdown_content += f"### {count}. 【{bot_name}】\n"
            markdown_content += f"- **詳細・導入リンク**: [{bot_name}のTop.ggページはこちら]({bot_url})\n"
            markdown_content += f"- **紹介**: 今Top.ggのトレンドにランクインしている注目のBotです。\n\n"
            
            # 最大20件まで引っこ抜く
            if count >= 20:
                break

    if count > 0:
        # 集めたデータを「index.md」という名前のファイルとしてパソコンに保存する
        with open("index.md", "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"成功！ {count}件のBotデータを『index.md』に保存しました。")
    else:
        print("Botが見つかりませんでした。")

except Exception as e:
    print(f"エラーが発生しました: {e}")
