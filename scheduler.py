# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Scheduler 

import schedule
from manager import log_event

def run_schedule():
    while True:
        schedule.run_pending()

#################
### Functions ###
#################

def clean_otp():
    """Cleans the OTP table."""
    from manager import clean_expired_otps
    removed_otps = clean_expired_otps()
    log_event(f"Removed {removed_otps} expired OTPs.")

#################
### Schedules ###
#################

schedule.every(2).seconds.do(clean_otp)

