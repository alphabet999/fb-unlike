from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
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
        print("Loading took too much time!")
        return 0

def total_pages_like(username):
    driver.execute_script("window.open('');")
    # Switch to the new window
    driver.switch_to.window(driver.window_handles[1])
    try:
        driver.get("https://www.facebook.com/"+username+"/likes")
        myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'All Likes')))
    except TimeoutException:
        print("Loading took too much time!")
    total_likes  = driver.find_element_by_name('All Likes')
    total_likes = total_likes.text
    total_likes = total_likes.replace('All Likes','')
    total_likes = total_likes.replace(",","")
    driver.close()
    # Switch back to the first tab
    driver.switch_to.window(driver.window_handles[0])
    return total_likes

def get_username():
    return sys.argv[0]

def get_all_links(username):
    driver.get("https://mbasic.facebook.com/"+username+"?v=likes")
    elems = driver.find_elements_by_xpath("//a[@href]")
    liked_page_list = list()
    for elem in elems:
        link = elem.get_attribute("href")
        regexes = [
            "/notes/",
            "/saved/",
            "/home.php/",
            "/messages/",
            "/notifications.php",
            "/buddylist.php",
            "/friends/",
            "/pages/",
            "/groups/",
            "/events/",
            "/settings/",
            "/help/",
            "/menu/",
            "/photo.php",
            "/"+username,
            "/allactivity",
            "/privacyx/",
            "v=likes",
            "/timeline/",
            "/bugnub/",
            "/policies/",
            "logout.php",
            "home.php"
            ]
        combined = "(" + ")|(".join(regexes) + ")"
        if not (re.search(combined, link)):
            liked_page_list.append(link)
    return liked_page_list

def unlike_page(page_url):
    status = 0
    driver.execute_script("window.open('');")
    # Switch to the new window
    driver.switch_to.window(driver.window_handles[1])
    driver.get(page_url)
    try:
        driver.find_element_by_partial_link_text('Unlike').click()
        status = status + 1
    except:
        pass

    driver.close()
    # Switch back to the first tab
    driver.switch_to.window(driver.window_handles[0])
    return status

def action(total_pages_like):
    total_pages_like = int(total_pages_like)
    print("Total Pages Liked: ",total_pages_like)

    if total_pages_like>0:
        liked_page_list = get_all_links(username)
        liked_page_list.reverse()
        refresh_list = len(liked_page_list)
        count = 0
        for i in range(0,refresh_list):
            status = unlike_page(liked_page_list[i])
            if status>0:
                sys.stdout.write("\r%d page unliked" % status)
                sys.stdout.flush()
    else:
        exit()

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
#options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)

if login(username,passw):
    total_pages_like = total_pages_like(username)
    action(total_pages_like)
    exit()
