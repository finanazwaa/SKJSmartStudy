from blocklist_loader import load_blocklist, is_blocked
from logging_system import log_alert
from notification_system import notify

def process_domain(domain):
    blocklist = load_blocklist()

    if is_blocked(domain, blocklist):
        log_alert(domain)
        notify(domain)

def test_detection():
    test_domains = ["google.com", "youtube.com", "steamcdn.com"]

    for domain in test_domains:
        process_domain(domain)

def integration_placeholder(member1_domain_generator):
    for domain in member1_domain_generator():
        process_domain(domain)

# Example usage
if __name__ == "__main__":
    test_detection()
    print("Mock detection test completed.")

    # Example placeholder usage (replace with real generator later)
    def mock_domain_generator():
        yield "example.com"
        yield "youtube.com"
        yield "tiktok.com"

    integration_placeholder(mock_domain_generator)
    print("Integration placeholder test completed.")

    #run python3 detection_module.py in command line to test the code

