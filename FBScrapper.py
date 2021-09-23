#!/usr/bin/python3
import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import urllib.request
import re

options = Options()
options.page_load_strategy = 'normal'
headers = 'user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
options.add_argument(headers)
driver = webdriver.Chrome(options=options)

# open the cookies jar
driver.get(
    'https://m.facebook.com/')
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

# it show time!
driver.get('') # insert your group member profile url here

# check if element by link text is exist
def check_element_by_link_text(link_text):
    try:
        driver.find_element_by_link_text(link_text)
    except NoSuchElementException:
        return False
    return True

def get_timestamp():
    # Get the post's time
    timestamp_raw = driver.find_element_by_tag_name(
        'abbr').get_attribute('innerHTML')
    if timestamp_raw == "":
        timestamp_raw = "Null"
    timestamp_non_alphanumeric = timestamp_raw.replace(" ", "_")
    timestamp = re.sub("[^0-9a-zA-Z]+", "_", timestamp_non_alphanumeric)
    return timestamp

def multipic_get_timestamp():
    timestamp_raw = driver.find_element_by_xpath(
        '/html/body/div[2]/div/div[2]/article/div/div/div[1]/div/div[1]/div[1]/div/div[2]/abbr').get_attribute('innerHTML').replace(" ", "_")
    timestamp = re.sub("[^0-9a-zA-Z]+", "_", timestamp_raw)
    return timestamp

def open_new_tab(url):
    # open the url to new page
    driver.execute_script(
        ''f"window.open('{url}','_blank');"'')
    # change focus to the second page
    window_name = driver.window_handles[-1]
    driver.switch_to.window(window_name=window_name)

def close_new_tab():
    driver.close()
    window_name = driver.window_handles[0]  # go back to the main window
    driver.switch_to.window(window_name=window_name)

def multipic_img_ids():
    current_url = driver.current_url
    current_url_start = current_url.find('fbid=')
    current_url_end = current_url.find('&id')
    current_url_fix = current_url[current_url_start + 
                                    5:current_url_end]
    return current_url_fix

# press the okay button if it get blocked by facebook
time.sleep(2)
if check_element_by_link_text('Okay'):
    driver.find_element_by_link_text('Okay').click()
    time.sleep(2)

# Get scroll height # https://tinyurl.com/uf6z66j2
last_height = driver.execute_script("return document.body.scrollHeight")

poster_count = 1
multipic_count = 5
while True:
# post with single image
    posts = driver.find_elements_by_class_name(
        "_39pi")
    poster = posts[poster_count]  # find the post with single image
    url = poster.get_attribute('href') # get the post url
    # print(url)
    open_new_tab(url)
    timestamp = get_timestamp() # get timestamp
    timestamp_format = f'./image/{timestamp}.jpg'
    view_full_size = driver.find_element_by_link_text(
        "View Full Size").get_attribute('href')  # Get the image URL
    driver.get(view_full_size)
    image_url = driver.find_element_by_tag_name('img').get_attribute('src')
    urllib.request.urlretrieve(
        image_url, timestamp_format)  # Download Image
    poster_count = poster_count + 1  # add 1 to the poster_count counter
    print('saving single', timestamp_format)
    time.sleep(1)  # slowdown for 1 sec and close the new page
    close_new_tab()
    time.sleep(0.5)

# post with multiple image
    multipic_url = driver.find_elements_by_class_name("_26ih")
    # print('nope it still', len(multipic_url))
    if len(multipic_url) > multipic_count:
        multipic_count = len(multipic_url)
        print('found multipic post in', multipic_count)
        multipic_url[multipic_count - 1].click()
        # wait for the page to load
        WebDriverWait(driver, 30).until(
            lambda x: x.find_element_by_class_name("_56be").is_displayed())
        the_images = driver.find_elements_by_class_name(
            "_56be")
        current_url = driver.current_url
        # get timestamp
        mutlipic_timestamp = multipic_get_timestamp()

        # fuck it going MBasic mode!
        mbasic_formater = current_url.replace('https://m', 'https://mbasic')
        # open the url to new page
        open_new_tab(mbasic_formater)
        time.sleep(1)
        driver.find_element_by_xpath(
            '/html/body/div/div/div[2]/div/div[1]/div[1]/a[1]').click()
        img_id_list = list()
        img_count = 0
        while True:
            current_url2 = multipic_img_ids()
            if current_url2 in img_id_list:
                print('last image, done!')
                break
            filename_format = f'./image/{mutlipic_timestamp}_{img_count}.jpg'
            img_id_list.append(current_url2)
            # print(current_url2)
            driver.find_element_by_xpath(
                '/html/body/div/div/div[2]/div/div[1]/div/div/div[1]/div/div[2]/table/tbody/tr/td[2]/a').click()
            fullsize_img_url = driver.find_element_by_xpath(
                '/html/body/div/div/div[2]/div/div[1]/div/div/div[3]/div[1]/div[2]/span/div/span/a[1]').get_attribute('href')
            print('saving multi', filename_format)
            driver.get(fullsize_img_url)
            image_url = driver.current_url
            # print(image_url) # image url
            driver.back()
            urllib.request.urlretrieve(
                image_url, filename_format)  # Download Image
            img_count = img_count + 1
            time.sleep(0.5)
        close_new_tab()
        driver.back()

    if (poster_count == len(posts)) and (len(multipic_url) == multipic_count):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(3)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print('we\'re done here this is the last pages!')
            break
        last_height = new_height
