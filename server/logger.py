# Lucas Mathews - Fontys Student ID: 5023572
# Banking System Logger

import datetime

def timestamp():
    """Returns the current timestamp in the format 'YYYY-MM-DD HH:MM:SS'."""
    return (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def event_logger(data_to_log:str):
    """Logs an event to the log file."""
    import os
    print(os.getcwd())
    with open("log.txt", "a") as log_file:
        log_file.write(f"{timestamp()} - {data_to_log}\n")