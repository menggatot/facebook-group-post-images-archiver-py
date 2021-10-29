#!/usr/bin/python3
import pickle
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
import urllib.request
import re
from pathlib import Path
from PIL import Image
import imagehash
import glob
import os

# driver = webdriver.Chrome('I:\Project\Python\chromeHeadless\chromedriver.exe')
options = Options()
options.page_load_strategy = 'normal'
options.add_argument('log-level=3')
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
headers = 'user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
options.add_argument(headers)
driver = webdriver.Chrome(options=options)

# open the cookies jar
driver.get(
    'https://m.facebook.com/')
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

# INSERT THE FACEBOOK GROUP'S USER URL HERE!
driver.get(
    'https://m.facebook.com/...')

# check if element by link text is exist
def check_element_by_link_text(link_text):
    try:
        driver.find_element_by_link_text(link_text)
    except NoSuchElementException:
        return False
    return True


def scroll_down():
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

def timestamp_raw_list():
    return driver.find_elements_by_tag_name('abbr')

def get_timestamp(i):
    timestamp_raw = timestamp_raw_list()[i].get_attribute(
        'innerHTML')
    if timestamp_raw == "":
        timestamp_raw = "Null"
    timestamp_non_alphanumeric = timestamp_raw.replace(" ", "_")
    timestamp = re.sub("[^0-9a-zA-Z]+", "_", timestamp_non_alphanumeric)
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


def click_next(current_url2):
    img_id_list.append(current_url2)
    # print(current_url2)
    driver.find_element_by_xpath(
        '/html/body/div/div/div[2]/div/div[1]/div/div/div[1]/div/div[2]/table/tbody/tr/td[2]/a').click()


def find_dublicate(trash_to_find):
    all_files = list(filter(os.path.isfile, glob.glob("image/*")))
    all_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    excludes = ['_Yesterday_', '_mins', '_hr']
    trashs = []
    i = 0
    for i in range(0, len(all_files)):
        for exlude in excludes:
            if exlude in all_files[i]:
                trashs.append(all_files[i])
    i = i+1

    what_it_found = []
    loop_count = 0
    while loop_count < len(trashs):
        try:
            hash0 = imagehash.average_hash(Image.open(trash_to_find))
            hash1 = imagehash.average_hash(Image.open(trashs[loop_count]))
            cutoff = 5  # maximum bits that could be different between the hashes.

            if hash0 - hash1 < cutoff:
                what_it_found.append(trashs[loop_count])
                print(f'found dublicate {trashs[loop_count]}')
                loop_count += 1
                continue
            else:
                loop_count += 1
                continue
        except FileNotFoundError:
            break
    for file in what_it_found:
        file_name = re.sub(r'^.*?\\', '', file)
        os.replace(file, f'dublicate/{file_name}')

# press the okay button if it get blocked by facebook
time.sleep(2)
if check_element_by_link_text('Okay'):
    driver.find_element_by_link_text('Okay').click()
    time.sleep(2)

# Get scroll height # https://tinyurl.com/uf6z66j2
last_height = driver.execute_script("return document.body.scrollHeight")

poster_count = 1
multipic_count = 5
timestamp_count = 0
title = str(driver.title).replace(" ", "_")
scroll_count = 0
while True:
    timestamp_elements = driver.find_elements_by_tag_name('abbr')

    # post with single image
    posts = driver.find_elements_by_class_name(
        "_39pi")
    # post with multiple image
    multipic_url = driver.find_elements_by_class_name("_26ih")

    if timestamp_count == len(timestamp_raw_list()):
        scroll_down()
        scroll_count += 1
        print(f'you\'re now at scroll count {scroll_count}')

    timestamp = get_timestamp(timestamp_count)

    file_timestamp = Path(
        f'image/{title}_{timestamp}*.jpg'
    )

    # change this value to change how many time it will scroll
    if scroll_count == 3:
        print('you\'re at the last line')
        driver.execute_script(
            "window.scrollTo(0, 0);")
        poster_count = 1
        multipic_count = 5
        timestamp_count = 0
        scroll_count = 0
        break # comment this and uncomment 2 line bellow this make the scrip loop
        # time.sleep(60) # how long the script need to wait
        # continue

    file_path_single = Path(f'image/{title}_{timestamp}.jpg')

    # print('nope it still', len(multipic_url))
    if len(multipic_url) > multipic_count:
        multipic_count = len(multipic_url)
        print('found multipic post in', multipic_count)
        multipic_url[multipic_count - 1].click()
        # wait for the page to load
        time.sleep(2)
        current_url = driver.current_url
        # print(timestamp, '\n', current_url, '\n\n')
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
            file_path_multipic = Path(
                f'image/{title}_{timestamp}_p{img_count}.jpg')
            current_url2 = multipic_img_ids()
            find_dublicate(file_path_multipic)
            if current_url2 in img_id_list:
                print('last image, done!')
                break
            if file_path_multipic.is_file():
                print(f'skipping {file_path_multipic} file exist')
                click_next(current_url2)
                img_count = img_count + 1
                continue
            click_next(current_url2)
            fullsize_img_url = driver.find_element_by_xpath(
                '/html/body/div/div/div[2]/div/div[1]/div/div/div[3]/div[1]/div[2]/span/div/span/a[1]').get_attribute('href')
            print('saving multi', file_path_multipic)
            driver.get(fullsize_img_url)
            image_url = driver.current_url
            # print(image_url) # image url
            driver.back()
            urllib.request.urlretrieve(
                image_url, file_path_multipic)  # Download Image
            img_count = img_count + 1
            time.sleep(0.5)
        close_new_tab()

        driver.back()
        timestamp_count = timestamp_count + 1
    else:  # post with single image
        find_dublicate(file_path_single)
        if file_path_single.is_file():
            print(f'skipping {file_path_single} file exist', timestamp_count)
            poster_count = poster_count + 1
            timestamp_count = timestamp_count + 1
            continue
        poster = posts[poster_count]  # find the post with single image
        url = poster.get_attribute('href')  # get the post url
        # print(timestamp, '\n', url, '\n\n')
        open_new_tab(url)
        view_full_size = driver.find_element_by_link_text(
            "View Full Size").get_attribute('href')  # Get the image URL
        driver.get(view_full_size)
        image_url = driver.find_element_by_tag_name('img').get_attribute('src')
        # print(image_url)
        urllib.request.urlretrieve(
            image_url, file_path_single)  # Download Image
        poster_count = poster_count + 1  # add 1 to the poster_count counter
        print('saving single', file_path_single)
        time.sleep(0.5)
        close_new_tab()
        timestamp_count = timestamp_count + 1
