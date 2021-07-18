# Function helper for testing purpose

def rowcnt_result(path):
    """Counting scraping result in ND-JSON format"""
    cnt = 0
    with open(path, "r") as f:
        for line in f:
            cnt += 1
    return cnt
