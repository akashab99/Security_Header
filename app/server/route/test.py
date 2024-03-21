import requests
from bs4 import BeautifulSoup

# List of common security headers
COMMON_SECURITY_HEADERS = [
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Content-Security-Policy",
    "X-XSS-Protection",
    "Strict-Transport-Security",
    "Permissions-Policy"
]


def scan_security_headers(url):
    try:
        response = requests.head(url)
        security_headers = {}
        for header_scan in COMMON_SECURITY_HEADERS:
            security_headers[header_scan] = response.headers.get(header_scan)
        return security_headers
    except requests.exceptions.RequestException as e:
        print("Error in scan_security_headers:", e)
        return {"Error" : "Unable to scan_security_headers"}


def find_missing_headers(headers_missing):
    missing_header_data = []
    for header_find in COMMON_SECURITY_HEADERS:
        if header_find not in headers_missing or not headers_missing[header_find]:
            missing_header_data.append(header_find)
    return missing_header_data

def get_directory_listing(url_given):
    try:
        response = requests.get(url_given)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href is not None and '/' in href and href.split('/', 1)[1] != '':
                    links.append(href)
            return links
        else:
            print(f"Failed to retrieve directory listing from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    url_input = input("Enter the URL to scan: ")
    headers = scan_security_headers(url_input)
    print("Security Headers:")
    for header, value in headers.items():
        print(f"{header}: {value}")

    missing_headers = find_missing_headers(headers)
    if missing_headers:
        print("\nMissing Security Headers:")
        for header in missing_headers:
            print(header)
    else:
        print("\nAll common security headers are present.")

    directory_listing = get_directory_listing(url_input)
    if directory_listing:
        print("\nDirectory listing:")
        for item in directory_listing:
            print(item)
