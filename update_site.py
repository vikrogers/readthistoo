import requests
import html
from datetime import datetime

API_KEY = "bf39c65adee34e8e9c7c3c434f58f4d3"
url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"

resp = requests.get(url)
data = resp.json()

if resp.status_code != 200 or not data.get("articles"):
    print("⚠️ Failed to fetch headlines:", data.get("message", ""))
    exit(1)

article = data["articles"][0]
headline = html.escape(article["title"])
story_url = article["url"]

# Quick real links to get you going
left_oped = "https://www.vox.com/"
right_oped = "https://www.wsj.com/"

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

print("✅ index.html updated with headline from NewsAPI.")
