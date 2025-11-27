import os
import platform

def notify(domain):
    """
    Sends a notification about a blocked domain based on the operating system.

    Args:
        domain (str): The domain that was detected as blocked.
    """
    system_platform = platform.system()

    if system_platform == "Windows":
        # Windows notification
        os.system(f'msg * ALERT: Blocked domain detected - {domain}')
    elif system_platform == "Linux":
        # Linux notification
        os.system(f"notify-send 'Blocked Domain' '{domain}'")
    elif system_platform == "Darwin":  # macOS
        # macOS notification
        os.system(f"osascript -e 'display notification \"{domain}\" with title \"Blocked Domain\"'")
    else:
        print(f"Notification not supported on this platform: {system_platform}")

# Example usage
if __name__ == "__main__":
    test_domain = "youtube.com"
    notify(test_domain)
    print(f"Notification sent for domain: {test_domain}")

    #run python3 notification_system.py in command line to test the code