from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import re
import sys

def login(username,passw):
    driver.get("https://mbasic.facebook.com")
    email = driver.find_element_by_name('email')
    email.send_keys(username)
    password = driver.find_element_by_name('pass')
    password.send_keys(passw)
    driver.implicitly_wait(10)
    password.submit()
    try:
        myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, 'nux_source')))
        driver.get("https://mbasic.facebook.com/login/save-device/cancel/?flow=interstitial_nux&nux_source=regular_login")
        return 1
    except TimeoutException:
        print("Not able to Login!")
        return 0

def total_pages_like(username):
    driver.execute_script("window.open('');")
    # Switch to the new window
    driver.switch_to.window(driver.window_handles[1])
    try:
        driver.get("https://www.facebook.com/"+username+"/likes")
        myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'All Likes')))
        total_likes  = driver.find_element_by_name('All Likes')
        total_likes = total_likes.text
        total_likes = total_likes.replace('All Likes','')
        total_likes = total_likes.replace(",","")
        if total_likes is not "":
            print("Total Pages Liked: ",total_likes)
    except:
        print("Can't Fetch No of Pages Liked!")

    driver.close()
    # Switch back to the first tab
    driver.switch_to.window(driver.window_handles[0])
    return total_likes

def get_username():
    return sys.argv[0]


def unlike_page(count = 0, refreshed = 1):
    try:
        driver.get("https://mtouch.facebook.com/pages/launchpoint/liked_pages/?ref=bookmarks&from=pages_nav_home")
        time.sleep(1)
    except TimeoutException:
        print("Failed to load!")

    elems = driver.find_elements_by_xpath("//a[@href]")
    if len(elems) is 0:
        return 0
    for elem in elems:
        link = elem.get_attribute("href")
        if "unfan" in link:
            if navigate_unfan(link):
                count = count + 1
                sys.stdout.write("\r%d page unliked" % count)
                sys.stdout.flush()

    refreshed = refreshed + 1
    unlike_page(count, refreshed)
    return 0

def navigate_unfan(link,status = 0):
    driver.execute_script("window.open('');")
    # Switch to the new window
    driver.switch_to.window(driver.window_handles[1])
    try:
        driver.get(link)
        status = 1
    except:
        print("Failed to load!")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return status

################################MAIN############################################
print("              ___ __                 ____")
print(" __  ______  / (_) /_____     ____ _/ / /")
print(" / / / / __ \/ / / //_/ _ \   / __ `/ / /")
print("/ /_/ / / / / / / ,< /  __/  / /_/ / / /")
print("\__,_/_/ /_/_/_/_/|_|\___/   \__,_/_/_/")

print("Example Usage: $python3 unlike.py -u fb-username -p fb-password")
################################MAIN############################################
if len(sys.argv)<5:
    exit()

if str(sys.argv[1]) == "-u":
    username = sys.argv[2]
else:
    print("Example Usage: $python3 unlike.py -u fb-username -p fb-password")
    exit()

if str(sys.argv[3]) == "-p":
    passw = sys.argv[4]
else:
    print("Example Usage: $python3 unlike.py -u fb-username -p fb-password")
    exit()

print(":unlike facebook pages:")
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

if login(username,passw):
    total_pages_like = total_pages_like(username)
    unlike_page()
    print("\nGood Bye!")
