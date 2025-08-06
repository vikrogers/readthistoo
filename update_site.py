import requests
import html
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.parse

API_KEY = "bf39c65adee34e8e9c7c3c434f58f4d3"
news_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

# Step 1: Get top headline
resp = requests.get(news_url)
data = resp.json()

if resp.status_code != 200 or not data.get("articles"):
    print("⚠️ Failed to fetch headlines:", data.get("message", ""))
    exit(1)

article = data["articles"][0]
raw_headline = article.get("title", "No headline").strip()
headline = html.escape(raw_headline)
story_url = article.get("url", "#")

print(f"📰 Headline: {headline}")
print(f"🔗 Article: {story_url}")

# Step 2: Define source lists
LEFT_SOURCES = ["vox.com", "msnbc.com", "slate.com", "motherjones.com", "theatlantic.com"]
RIGHT_SOURCES = ["foxnews.com", "wsj.com", "nypost.com", "nationalreview.com", "dailywire.com"]

def search_google_news(query, bias_list):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        q = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={q}&tbm=nws"
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "url?q=" in href:
                link = href.split("url?q=")[1].split("&")[0]
                for domain in bias_list:
                    if domain in link:
                        return link
    except Exception as e:
        print(f"⚠️ Error searching Google: {e}")
    return None

# Step 3: Get matching op-eds
left_oped = search_google_news(raw_headline, LEFT_SOURCES) or "https://www.vox.com/"
right_oped = search_google_news(raw_headline, RIGHT_SOURCES) or "https://www.wsj.com/"

print(f"🔵 Left-leaning article: {left_oped}")
print(f"🔴 Right-leaning article: {right_oped}")

# Step 4: Build HTML
new_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Read This Too</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header>
    <h1>Read This Too</h1>
    <p>Every story has two sides. Here’s both.</p>
  </header>

  <main>
    <h2>Today's Story – {datetime.utcnow().strftime('%B %d, %Y')}</h2>
    <p><strong>Headline:</strong> <a href="{story_url}" target="_blank">{headline}</a></p>
    <div class="links">
      <a href="{left_oped}" target="_blank" class="left">Read the left-leaning op-ed</a>
      <a href="{right_oped}" target="_blank" class="right">Read the right-leaning op-ed</a>
    </div>
  </main>

  <footer>
    <p>© 2025 ReadThisToo.com</p>
  </footer>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("✅ Site updated successfully.")
