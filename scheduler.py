import time
import schedule


def run_job_bot():
  print("Running job scraper and sending alert...")
  # Yahan aap apna main.py ka code ya function call kar sakte hain
  # jaise: import main


# Har 6 ghante me ek baar run karega
schedule.every(6).hours.do(run_job_bot)

# Ya roz subah 9:00 baje fix time par:
# schedule.every().day.at("09:00").do(run_job_bot)

print("Job Scheduler started successfully. Waiting for schedule...")

while True:
  schedule.run_pending()
  time.sleep(1)