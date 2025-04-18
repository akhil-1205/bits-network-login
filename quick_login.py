# quick_login.py
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Load credentials from the JSON file
def load_credentials():
    CREDENTIALS_FILE = "credentials.json"
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as f:
            data = json.load(f)
            return data.get("username", ""), data.get("password", "")
    return "", ""

# Perform the login action
def login_to_website(username, password):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://172.16.0.30:8090/httpclient.html")
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.ID, "loginbutton").click()
        driver.quit()
    except Exception as e:
        print(f"Error during login: {e}")

if __name__ == "__main__":
    username, password = load_credentials()
    if username and password:
        login_to_website(username, password)
    else:
        print("No credentials found. Please set them first.")
