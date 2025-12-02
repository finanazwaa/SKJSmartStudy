import os
from datetime import datetime

def log_alert(domain, log_file="logs/alerts.log"):
    """
    Logs a blocked domain detection event to a log file.

    Args:
        domain (str): The domain that was detected as blocked.
        log_file (str): Path to the log file. Defaults to "logs/alerts.log".
    """
    # Ensure the logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # Append the log entry to the file
    with open(log_file, "a") as f:
        f.write(f"[{datetime.now()}] BLOCKED DOMAIN DETECTED: {domain}\n")

# Real main usage
if __name__ == "__main__":
    domains_to_log = ["youtube.com", "example.com", "blockedsite.com"]
    for domain in domains_to_log:   
        log_alert(domain)
        print(f"Logged alert for domain: {domain}")

    #run python3 logging_system.py in command line to test the code
    #run cat logs/alerts.log to see the log entries
    #run python3 logging_system.py to test
