import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Step 1: Get top Reuters headline
reuters_url = "https://www.reuters.com/news/archive/topNews"
html = requests.get(reuters_url).text
soup = BeautifulSoup(html, "html.parser")

# Find first headline
headline_tag = soup.find("h3", class_="story-title")
if not headline_tag:
    headline_tag = soup.find("a", {"href": True})

if not headline_tag or not headline_tag.text.strip():
    print("⚠️ Could not find a valid headline. Exiting.")
    exit(1)

headline = headline_tag.text.strip()
href = headline_tag.find_parent("a")["href"] if headline_tag.find_parent("a") else headline_tag["href"]
story_url = "https://www.reuters.com" + href

# Step 2: Placeholder op-eds
left_oped = "https://left.example.com/"
right_oped = "https://right.example.com/"

# Step 3: Build updated HTML content
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

# Step 4: Save to index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("✅ index.html updated with Reuters headline.")
