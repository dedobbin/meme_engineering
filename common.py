from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests
import cv2
import numpy as np

def get_web_driver(debug: bool = False):
    chrome_options = Options()

    if not debug:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu") #https://bugs.chromium.org/p/chromium/issues/detail?id=737678
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    return driver

def sanity_check_driver_web_driver(webdriver):
    url = "https://www.python.org/"
    webdriver.get(url)
    print("Got '%s', title is '%s'" % (url, webdriver.title));


def url_to_img(url):
    raw = requests.get(url, stream=True).raw
    image = np.asarray(bytearray(raw.read()), dtype="uint8")
    return cv2.imdecode(image, cv2.IMREAD_COLOR)


# For checking if HTML responses etc are ok
def to_file(input: str, output_file_path: str = "output.html"):
    with open(output_file_path, "w") as f:
        f.write(input.text)

def generate_imgs(n):
    # [val] * n won't work because all n items are pointing to same memory..
    res = []
    for i in range(n):
        res.append(np.random.randint(255, size=(900,800,3),dtype=np.uint8))
    return res