import requests
from bs4 import BeautifulSoup
from common import url_to_img

class tumblr:
    @staticmethod
    def get_image_from_profile(profile:str, max: int = 0):
        profile_html: str = requests.get("http://www.%s.tumblr.com" % profile).text
        soup = BeautifulSoup(profile_html, 'html.parser')
        img_elements = soup.select('[src*="64.media.tumblr.com"]')
        img_elements = img_elements if max == 0 else img_elements[:max]
        imgs = list(map(lambda x: url_to_img(x["src"]), (img_elements)))
        return imgs