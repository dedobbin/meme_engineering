from common import url_to_img, generate_img
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import os
import logging

def cookie_popup(driver, max_time = 3):
    try:
        button = WebDriverWait(driver, max_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[title*=Cookies]")))
        button.click()
        return True
    except TimeoutException:
        #@todo: logger
        print("Could not find cookie popup to close")
        return False

class facebook:
    @staticmethod
    def get_images_from_profile(driver, profile, max=0):
        if not os.environ.get("REAL_FB", "false").lower() == "true":
            logging.warning("Mocking images from Facebook - put `REAL_FB=true` in .env for real requests")
            return [generate_img(), generate_img(), generate_img()]
        else:
            #@todo: scroll down for more images
            driver.get("https://www.facebook.com/%s" % profile)
            cookie_popup(driver)
            sleep(1) 
            img_elements = driver.find_elements_by_css_selector("[rel=theater] img")
            img_elements = img_elements if max == 0 else img_elements[:max]
            return list(map(lambda x: url_to_img(x.get_attribute("src")), (img_elements)))


