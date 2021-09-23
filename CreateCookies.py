import pickle
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.get(
    'https://m.facebook.com/')
WebDriverWait(driver, 30).until(
    lambda x: x.find_element_by_class_name("story_body_container").is_displayed())
pickle.dump(driver.get_cookies(), open("./cookies.pkl", "w+b"))
driver.close()
