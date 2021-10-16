import requests
from bs4 import BeautifulSoup
from common import url_to_img
import logging
from common import generate_img
import os

class tumblr:
    @staticmethod
    def get_images_from_profile(profile:str, max: int = 0):
        if not os.environ.get("REAL_TUMBLR", "false").lower() == "true":
            logging.warning("Mocking images from Instagram - put `REAL_TUMBLR=true` in .env for real requests")
            return [generate_img(), generate_img(), generate_img()]
        else:      
            profile_html: str = requests.get("http://www.%s.tumblr.com" % profile).text
            soup = BeautifulSoup(profile_html, 'html.parser')
            img_elements = soup.select('[src*="64.media.tumblr.com"]')
            img_elements = img_elements if max == 0 else img_elements[:max]
            imgs = list(map(lambda x: url_to_img(x["src"]), (img_elements)))
            return imgs