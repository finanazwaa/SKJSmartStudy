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
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Append the log entry to the file
    with open(log_file, "a") as f:
        f.write(f"[{datetime.now()}] BLOCKED DOMAIN DETECTED: {domain}\n")

# Example usage
if __name__ == "__main__":
    test_domain = "youtube.com"
    log_alert(test_domain)
    print(f"Logged alert for domain: {test_domain}")

    #run python3 logging_system.py in command line to test the code
    #run cat logs/alerts.log to see the log entries