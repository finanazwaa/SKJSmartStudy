def log_alert(domain):
    print(f"Alert: {domain} is blocked.")

def is_blocked(domain, blocklist):
    return domain in blocklist  # Example implementation

def notify(domain):
    print(f"Notification: {domain} has been blocked.")

blocklist = ["youtube.com", "tiktok.com", "discord.com"]  # Example blocklist

def process_domain(domain):
    if is_blocked(domain, blocklist):
        log_alert(domain)  # Log the blocked domain
        notify(domain)  # Send a notification (optional)

# Add this block to execute the script
if __name__ == "__main__":
    test_domains = ["google.com", "youtube.com", "example.com"]
    for domain in test_domains:
        process_domain(domain)
