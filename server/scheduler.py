# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Scheduler 

import threading
import schedule
import time
from manager import event_logger

stop_event = threading.Event()

def run_schedule():
    while not stop_event.is_set():
        schedule.run_pending()
        time.sleep(1)  # Add a short sleep to reduce CPU usage

def clean_otp():
    """Cleans the OTP table."""
    print("Cleaning OTPs...")
    from manager import clean_expired_otps
    removed_otps = clean_expired_otps()
    event_logger(f"Removed {removed_otps} expired OTPs.")

schedule.every(300).seconds.do(clean_otp) 

thread = threading.Thread(target=run_schedule)
thread.daemon = True  # Set the thread as a daemon thread
thread.start()

try:
    while True:  # Keep the main program running
        time.sleep(1)
except KeyboardInterrupt:
    stop_event.set()  # Signal the thread to stop