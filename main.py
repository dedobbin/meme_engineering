from tumblr import tumblr
from facebook import facebook
from automatic_watermarker import automatic_watermarker
import cv2
from random import choice
from string import ascii_uppercase
import os
from common import get_web_driver,sanity_check_driver_web_driver
from hash_tagger import tag_image
from db import get_db_reference, store
from dotenv import load_dotenv
import logging
import json

def get_sources(file: str ="./sources.json"):
    
    def parse_entry(entry):
        if "watermarks" in entry:
            entry["watermark"] = entry["watermarks"]
        return entry

    with open(file) as json_file:
        return list(map (parse_entry, json.load(json_file)))
    
def mark_and_store_images(imgs, watermark, db=None, output_path=None):
    if not db:
        logging.warning("Won't store images to DB")

    for img in imgs:
        energy = automatic_watermarker.forward_energy(img)
        #cv2.imwrite("Features.jpg", energy)
        zone = automatic_watermarker.findDark(energy)

        watermark_path = get_watermark_path(choice(watermark) if isinstance(watermark, list) else watermark)
        if not watermark_path:
            logging.error("Cannot find watermark %s" % watermark_path)
            continue

        watermarked_image = automatic_watermarker.addWatermark(zone, img, watermark_path)
        tagged_image, img_hash = tag_image(watermarked_image)

        if db:
            store(db, img_hash, "{Ayyy}")

        if output_path:
            total_output_path = "%s/%s/%s.png" % (str(os.getcwd()), output_path, ''.join(choice(ascii_uppercase) for i in range(12)))
            cv2.imwrite(total_output_path, tagged_image)

def get_watermark_path(name: str):
    path = "./automatic_watermarker/watermarks/%s.png" % name
    if not os.path.isfile(path):
        return None
    return path

def main(): 
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    load_dotenv() 
    
    driver = get_web_driver(True)
    #db = get_db_reference()
    db = None

    for source in get_sources():
        if not "url" in source or not "watermark" in source:
            logging.error("Entry from sources file does not contain URL and watermark")
            continue

        imgs = []
        if "facebook" in source["url"]:
            imgs = facebook.get_images_from_profile(url=source["url"], driver=driver, max_n=5)
        elif "tumblr" in source["url"]:
            imgs = tumblr.get_images_from_profile(url=source["url"], max_n=5)
        else:
            logging.error("Unknown website, %s" % source["url"])
            continue

        mark_and_store_images(imgs, source["watermark"], db=db, output_path="watermarked_images")

if __name__ == "__main__":
    main()