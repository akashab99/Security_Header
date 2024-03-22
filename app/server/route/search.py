# Third Party imports
import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, request, jsonify

# Define a blueprint
search_page = Blueprint('search_page', __name__)

# Define a route
@search_page.route('/')
def index():
    return render_template('user.html')


# data request route
@search_page.route('/url_scan', methods=['POST'])
def scan_validation():
    value_received = request.form['value']
    url_input = value_received
    headers = scan_security_headers(url_input)
    print(headers)
    # for header, value in headers.items():
    #     print(f"{header}: {value}")

    missing_headers = find_missing_headers(headers)
    if missing_headers:
        print(missing_headers)
        missing_headers_value = missing_headers
        # for header in missing_headers:
        #     print(header)
    else:
        missing_headers_value = ["All common security headers are present."]
        print("\nAll common security headers are present.")

    directory_listing = get_directory_listing(url_input)
    if directory_listing:
        directory_listing_value = directory_listing
    else:
        directory_listing_value = ["No Directory listing"]
        # for item in directory_listing:
        #     print(item)
    return jsonify({"data_value1": headers, "data_value2": missing_headers_value, "data_value3": directory_listing_value })


# List of common security headers
COMMON_SECURITY_HEADERS = [
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Content-Security-Policy",
    "X-XSS-Protection",
    "Strict-Transport-Security",
    "Permissions-Policy"
]


# scan_security_headers for url
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


# missing headers
def find_missing_headers(headers_missing):
    missing_header_data = []
    for header_find in COMMON_SECURITY_HEADERS:
        if header_find not in headers_missing or not headers_missing[header_find]:
            missing_header_data.append(header_find)
    return missing_header_data


# directory listing function
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

