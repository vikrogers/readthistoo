import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Get top AP News headline
ap_url = "https://apnews.com/hub/ap-top-news"
ap_html = requests.get(ap_url).text
soup = BeautifulSoup(ap_html, "html.parser")
headline_tag = soup.find("a", class_="PagePromo-link")
headline = headline_tag.text.strip()
story_url = "https://apnews.com" + headline_tag["href"]

# Fake op-eds for now (real scraping is next phase)
left_oped = "https://www.vox.com/"
right_oped = "https://www.wsj.com/"

# Build new HTML
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

# Overwrite index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)
