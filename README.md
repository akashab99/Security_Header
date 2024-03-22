# Security Header Application & Directory Listing

## Overview
This application provides security headers to enhance the security posture of web applications and includes a directory listing feature for managing files and directories within a web server environment.

## Features
1. **Security Headers**: Automatically injects security headers into HTTP responses to protect against common web vulnerabilities such as Cross-Site Scripting (XSS), Clickjacking, Content-Type sniffing, and more.
   
2. **Directory Listing**: Provides a user-friendly interface for browsing files and directories within a specified root directory on a web server. This feature enhances file management and navigation capabilities.


## Installation:
- ### Environment:
- Create an environment.
  - python -m venv env.
- Actiavte the environment.
  - "env/Scripts/activate".
- Go to the App directory.

## Requirements
- Install the required packages.
  - pip install -r requirements.txt

## Run the Application
- flask run --port=9000
