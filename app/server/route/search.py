# Third Party imports
import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, request, jsonify
import builtwith
import whois

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

    # Directory Listing
    directory_listing_value = []
    common_directories = ["admin", "uploads", "images", "css", "js"]
    for directory in common_directories:
        directory_data = get_directory_listing(url_input, directory)
        if directory_data:
            print(f"Data retrieved from directory '{directory}':")
            directory_listing_value.append(str(directory_data.decode("utf-8")))
        else:
            print(f"Directory '{directory}' does not exist.")
            directory_listing_value.append(f"Directory '{directory}' does not exist.")

    website_information = get_website_info(url_input)
    return jsonify({"data_value1": headers, "data_value2": missing_headers_value, "data_value3": directory_listing_value , "data_value4" : website_information})


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
def get_directory_listing(url_given, directory):
    try:
        target_url = f"{url_given}/{directory}"
        response = requests.get(target_url)
        if response.status_code == 200:
            return response.content
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")

def get_website_info(url):
    try:
        # Fetch webpage
        response = requests.get(url)
        if response.status_code == 200:
            # Analyze technologies using BuiltWith
            tech_info = builtwith.parse(url)
            print("Technologies used:")
            web_info = []
            for key, value in tech_info.items():
                web_info.append(f"{key}: {value}")

            # WHOIS lookup to find hosting provider
            domain = url.split('//')[-1].split('/')[0]
            domain_info = whois.whois(domain)
            web_info.append(domain_info.registrar)
            print("Hosting Provider:", domain_info.registrar)
            return web_info
        else:
            print("Failed to fetch the webpage. Status code:", response.status_code)
            return ["Failed to fetch the webpage."]
    except Exception as e:
        print("An error occurred:", str(e))


