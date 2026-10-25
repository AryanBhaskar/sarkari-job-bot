from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "8665128570:AAFUz8jxlQeezJZBm82tJ_bF4_MJotsYBxw"  # Replace with your token from BotFather
TELEGRAM_CHAT_ID = "5215149949"  # Replace with your ID from @userinfobot

# Target URL for Sarkari Result Latest Jobs
url = "https://www.sarkariresult.com/latestjob/"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )
}

# Your qualification keywords
target_keywords = [
    "graduate",
    "graduation",
    "computer",
    "technical",
    "engineer",
    "b.tech",
    "bca",
    "bsc",
    "b.com",
    "m.tech",
    "mca",
    "mba",
    "officer",
    "assistant",
    "je ",
    "clerk",
    "deo",
    "data entry",
    "accountant",
    "sci",
    "law",
]

print("Fetching active jobs...")

try:
  response = requests.get(url, headers=headers)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")

    active_matched_jobs = []
    today = datetime.now()

    for link in links:
      job_text = link.get_text(strip=True)
      job_url = link.get("href", "")

      if len(job_text) < 5:
        continue

      job_text_lower = job_text.lower()
      is_relevant = any(
          keyword in job_text_lower for keyword in target_keywords
      )

      if is_relevant:
        date_match = re.search(
            r"last\s*date\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})", job_text_lower
        )
        if date_match:
          date_str = date_match.group(1)
          try:
            expiry_date = datetime.strptime(date_str, "%d/%m/%Y")
            if expiry_date >= today:
              if not any(job[0] == job_text for job in active_matched_jobs):
                active_matched_jobs.append((job_text, job_url, date_str))
          except ValueError:
            pass

    # Limit to top 5 jobs
    active_matched_jobs = active_matched_jobs[:5]

    if active_matched_jobs:
      # Format message using Markdown style for Telegram
      message = "🚨 *New Active Jobs For You* 🚨\n\n"
      for idx, (title, link, expiry) in enumerate(active_matched_jobs, 1):
        message += (
            f"*{idx}. {title}*\n📅 Deadline: {expiry}\n🔗 [Apply Here]"
            f"({link})\n\n"
        )

      # Send message via Telegram Bot API
      telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
      payload = {
          "chat_id": TELEGRAM_CHAT_ID,
          "text": message,
          "parse_mode": "Markdown",
          "disable_web_page_preview": True,
      }

      tg_response = requests.post(telegram_url, json=payload)
      if tg_response.status_code == 200:
        print("Telegram alert sent successfully to your phone!")
      else:
        print(f"Failed to send Telegram message: {tg_response.text}")

    else:
      print("No active matching jobs found.")

  else:
    print(f"Failed to load page. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")