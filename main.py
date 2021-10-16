from tumblr import tumblr
from facebook import facebook
from automatic_watermarker import automatic_watermarker
import cv2
import numpy as np
from random import choice
from string import ascii_uppercase
import os
from common import get_web_driver,sanity_check_driver_web_driver
import pathlib
from glob import glob as find_file_names
from hash_tagger import get_db_reference, hash_tag_image, tag_and_upload_image_hash
from dotenv import load_dotenv
import logging

#added the db parameter to give a refernce to the firebase db to upload the info to
#it's not pretty but i need to have access to the watermarked image before upload
def watermark_to_disk(imgs, output_folder, watermark_list, db):
    if not os.path.exists(output_folder):
        pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    watermark_list= find_file_names("./automatic_watermarker/watermarks/*.png")

    for img in imgs:
        watermark_name = choice(watermark_list)
        energy = automatic_watermarker.forward_energy(img)
        #cv2.imwrite("Features.jpg", energy)
        zone = automatic_watermarker.findDark(energy)
        finalImage = automatic_watermarker.addWatermark(zone, img,watermark_name)
        
        finalImage = tag_and_upload_image_hash(db, finalImage, "{Ayyy}")

        #total_output_path = "%s/%s/%s" % (str(os.getcwd()), output_folder, ''.join(choice(ascii_uppercase) for i in range(12)) + ".png")
        #cv2.imwrite(total_output_path, finalImage)

def main(): 
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    load_dotenv() 
    possible_water_marks = find_file_names("./automatic_watermarker/watermarks/*.png")
    db = get_db_reference()

    driver = get_web_driver(True)
    imgs = facebook.get_images_from_profile(driver,"memes", max=10)
    watermark_to_disk(imgs, "output/facebook", possible_water_marks, db)

    imgs = tumblr.get_image_from_profile("sweetoothgirl", max=3)
    watermark_to_disk(imgs, "output/tumblr", possible_water_marks, db)

if __name__ == "__main__":
    main()