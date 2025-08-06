import requests
import html
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.parse

API_KEY = "bf39c65adee34e8e9c7c3c434f58f4d3"
news_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

# Step 1: Get headline
resp = requests.get(news_url)
data = resp.json()

if resp.status_code != 200 or not data.get("articles"):
    print("⚠️ Failed to fetch headlines:", data.get("message", ""))
    exit(1)

article = data["articles"][0]
raw_headline = article["title"]
headline = html.escape(raw_headline.strip()) if raw_headline else "No headline available"
story_url = article["url"]

print(f"📰 Headline: {headline}")
print(f"🔗 Original article: {story_url}")

# Step 2: Define source bias lists
LEFT_SOURCES = ["vox.com", "msnbc.com", "slate.com", "motherjones.com", "theatlantic.com"]
RIGHT_SOURCES = ["foxnews.com", "wsj.com", "nypost.com", "nationalreview.com", "dailywire.com"]

def search_google_news(query, bias_list):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    q = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={q}&tbm=nws"
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "url?q=" in href:
            link = href.split("url?q=")[1].split("&")[0]
            for domain in bias_list:
                if domain in link:
                    return link
    return None

# Step 3: Find relevant left and right links
left_oped = search_google_news(raw_headline, LEFT_SOURCES) or "https://www.vox.com/"
right_oped = search_google_news(raw_headline, RIGHT_SOURCES) or "https://www.wsj.com/"

print(f"🔵 Left link: {left_oped}")
print(f"🔴 Right link: {right_oped}")

# Step 4: Generate HTML
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

# Step 5: Write to file
with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("✅ index.html updated successfully.")
