import requests
from bs4 import BeautifulSoup
import numpy as np
import cv2

class tumblr:
    @staticmethod
    def get_image_from_profile(profile:str, n: int):
        profile_html: str = requests.get("http://www.%s.tumblr.com" % profile).text
        soup = BeautifulSoup(profile_html, 'html.parser')
        img_elements = soup.select('[src*="64.media.tumblr.com"]')
        img_elements = img_elements[:]
        imgs = list(map(lambda x: url_to_img(x["src"]), (img_elements)))
        return imgs


def url_to_img(url):
    raw = requests.get(url, stream=True).raw
    image = np.asarray(bytearray(raw.read()), dtype="uint8")
    return cv2.imdecode(image, cv2.IMREAD_COLOR)


# For checking if HTML responses etc are ok
def to_file(input: str, output_file_path: str = "output.html"):
    with open(output_file_path, "w") as f:
        f.write(input.text)

        