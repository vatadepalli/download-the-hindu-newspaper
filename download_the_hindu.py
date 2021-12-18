###############################################################################
# Author: @vatadepalli
# A simple script to download the latest The Hindu newspaper
# Usage - python3 download_the_hindu.py <login_email> <login_password>
# Output - File downloaded in the current directory
# Note - If the file fails to download completely, please increase download_timeout
###############################################################################

import pathlib
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# Time to wait for download to complete
download_timeout = 30

try:
  user_name = sys.argv[1]
except IndexError:
  print("Please provide a username as first argument\n ...and password as second argument")
  raise SystemExit

try:
  password = sys.argv[2]
except IndexError:
  print("Please provide your password - as second argument")
  raise SystemExit


# Not needed as ...vatadepalli/bin already in PATH
# chromedriver_path = "/Users/vatadepalli/bin/chromedriver"

options = Options()
options.add_argument("--window-size=1920x1080")
options.add_argument("--verbose")
options.add_argument("--headless")
options.add_experimental_option("prefs", {
    "download": {
        "default_directory": pathlib.Path().resolve().as_posix(),
    }
})

driver = webdriver.Chrome(
        options=options, 
        # chromedriver_path=executable_path
    )

print("Starting session...")

driver.get("https://epaper.thehindu.com/")
login_button = driver.find_element(By.CSS_SELECTOR, "body > nav.navbar.navbar-custom > div > ul > li:nth-child(4)")
login_button.click()

# wait for the login iframe to load
time.sleep(3)

# handle iframe with dynamic attributes
login_iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[title|=piano]"))
    )

print("Logging in...")
# switch to the login iframe
driver.switch_to.frame(login_iframe.get_attribute("name"));

# enter email
driver.find_element(By.ID, 'email').send_keys(user_name)
driver.find_element(By.CSS_SELECTOR, 'body > app-main > app-widget > screen-layout > main > current-screen > div > screen-login > p:nth-child(7) > button').click()

# wait for & enter password & proceed to login
WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#pass-field-2"))
    ).send_keys(password)
driver.find_element(By.CSS_SELECTOR, 'body > app-main > app-widget > screen-layout > main > current-screen > div > screen-login > p:nth-child(8) > button > span > t').click()

# download edition
download_button = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#edition_download"))
)[0]

print("Downloading, please wait...")
time.sleep(4)
download_button.click()
time.sleep(download_timeout)
print("Download complete!")

# Kill the driver
driver.close()
