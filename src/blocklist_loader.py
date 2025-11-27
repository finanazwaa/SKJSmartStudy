def load_blocklist(file_path="blocklist.txt"):
    """
    Reads the blocklist from the specified file and returns a list of blocked domains.

    Args:
        file_path (str): Path to the blocklist file. Defaults to "blocklist.txt".

    Returns:
        list: A list of blocked domains as strings.
    """
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines()]

def is_blocked(domain, blocklist):
    """
    Checks if a given domain is blocked based on the blocklist.

    Args:
        domain (str): The domain to check.
        blocklist (list): The list of blocked domains.

    Returns:
        bool: True if the domain is blocked, False otherwise.
    """
    return any(blocked in domain for blocked in blocklist)

# Example usage
if __name__ == "__main__":
    blocklist = load_blocklist()
    print("Loaded blocklist:", blocklist)

    test_domain = "youtube.com"
    print(f"Is '{test_domain}' blocked? {is_blocked(test_domain, blocklist)}")
    print(is_blocked("youtube.com", blocklist))  # True

    #run python3 blocklist_loader.py in command line to test the code