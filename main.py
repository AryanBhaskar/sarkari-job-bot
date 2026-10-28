import requests
from bs4 import BeautifulSoup

# --- DIRECT CONFIGURATION ---
TELEGRAM_BOT_TOKEN = "8665128570:AAFUz8jxlQeezJZBm82tJ_bF4_MJotsYBxw"
TELEGRAM_CHAT_ID = "5215149949"

# Target URL for Sarkari Result Latest Jobs
url = "https://www.sarkariresult.com/latestjob/"

# Enhanced headers to bypass 403 blocking
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.sarkariresult.com/",
    "Connection": "keep-alive",
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
    response = requests.get(url, headers=headers, timeout=15)
    print(f"Website Response Status: {response.status_code}")

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")

        active_matched_jobs = []

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
                if not any(job[0] == job_text for job in active_matched_jobs):
                    if job_url:
                        if job_url.startswith("/"):
                            job_url = "https://www.sarkariresult.com" + job_url
                        active_matched_jobs.append((job_text, job_url))

        # Limit to top 5 relevant jobs
        active_matched_jobs = active_matched_jobs[:5]
        print(f"Total matching jobs found: {len(active_matched_jobs)}")

        if active_matched_jobs:
            message = "🚨 *New Matching Jobs For You* 🚨\n\n"
            for idx, (title, link) in enumerate(active_matched_jobs, 1):
                message += f"*{idx}. {title}*\n🔗 [Apply Here]({link})\n\n"

            telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True,
            }

            tg_response = requests.post(telegram_url, json=payload)
            print(f"Telegram API Response Status: {tg_response.status_code}")

            if tg_response.status_code == 200:
                print("Telegram alert sent successfully to your phone!")
            else:
                print(f"Failed to send Telegram message: {tg_response.text}")
        else:
            print("No matching jobs found with current keywords.")
    else:
        print(f"Failed to load page. Status code: {response.status_code}")

except Exception as e:
    print(f"An error occurred: {e}")
