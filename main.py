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

def watermark_and_store_images_from(source, db=None, output_path=None):
    if not db:
        logging.warning("Won't store images to DB")
    
    imgs = get_images_from(source)
    for img in imgs:
        energy = automatic_watermarker.forward_energy(img)
        #cv2.imwrite("Features.jpg", energy)
        zone = automatic_watermarker.findDark(energy)
        watermarked_image = automatic_watermarker.addWatermark(zone, img, source["watermark"])
        tagged_image = tag_image(watermarked_image)

        if db:
            store(db, tagged_image, "{Ayyy}")

        if output_path:
            total_output_path = "%s/%s/%s.png" % (str(os.getcwd()), output_path, ''.join(choice(ascii_uppercase) for i in range(12)))
            cv2.imwrite(total_output_path, tagged_image)

def get_images_from(source):
    return source["callback"](*source["params"])

def water_mark_path(name: str):
    return "./automatic_watermarker/watermarks/%s.png" % name

def main(): 
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    load_dotenv() 
    
    driver = get_web_driver(True)

    sources = [
        {
            "callback": facebook.get_images_from_profile,
            "params": {"profile":"memes", "driver":driver},
            "watermark": water_mark_path("Trollface"),
        }, 
        {
            "callback": tumblr.get_images_from_profile,
            "params": {"profile":"sweetoothgirl"},
            "watermark": water_mark_path("Trollface"),
        }, 
    ]
    
    db = get_db_reference()
    for source in sources:
        watermark_and_store_images_from(source=source, db=db, output_path="watermarked_images")

if __name__ == "__main__":
    main()