import json

# Function helper for testing purpose

def rowcnt_result(path):
    """Counting scraping result in ND-JSON format"""
    cnt = 0
    with open(path, "r") as f:
        for line in f:
            cnt += 1
    return cnt

def print_title_url(path, start=1, end=-1):
    """Print all scraped news title and url from result in ND-JSON format from news number 'start' to 'end' (use 1-indexing)"""

    with open(path, "r") as f:
        for id, line in enumerate(f):
            if (id+1 <= start):
                continue

            # Print news
            news = json.loads(line)
            title_cln = news["title"].strip()
            url_cln = news["url"].strip()
            print(id, title_cln, url_cln, sep=" | ")

            if (id == end):
                break

def check_duplicate(path):
    """Check duplicate data (by name and url) and print their id (if duplicate exists)"""
    checked = set()
    hash_map = {}
    l = 0
    with open(path, "r") as f:
        for id, line in enumerate(f):
            # Extract news
            news = json.loads(line)
            title = news["title"].strip()
            url = news["url"].strip()

            # Add to checked and hashed. If duplicate detected, print their ID, title and URL
            checked.add((title, url))
            l += 1
            if (l > len(checked)):
                print("Duplicate:")
                print(f"News ID : {hash_map[title, url]} and {id}")
                print(f"Title : {title}\nURL : {url}")
                return False;
            else:
                hash_map[(title, url)] = id+1

    # No duplicate detected
    print("No Duplicate")
    return True
