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

def watermark_to_disk(imgs, output_folder):
    if not os.path.exists(output_folder):
        pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    for img in imgs:
        watermark_name = "./automatic_watermarker/Trollface.png"
        energy = automatic_watermarker.forward_energy(img)
        #cv2.imwrite("Features.jpg", energy)

        zone = automatic_watermarker.findDark(energy)
        finalImage = automatic_watermarker.addWatermark(zone, img,watermark_name)
        total_output_path = "%s/%s/%s" % (str(os.getcwd()), output_folder, ''.join(choice(ascii_uppercase) for i in range(12)) + ".png")
        print("Writing to %s" % total_output_path)
        cv2.imwrite(total_output_path, finalImage)

def main(): 
    driver = get_web_driver(True)
    imgs = facebook.get_images_from_profile(driver,"memes", max=3)
    watermark_to_disk(imgs, "output/facebook")

    imgs = tumblr.get_image_from_profile("sweetoothgirl", max=3)
    watermark_to_disk(imgs, "output/tumblr")

if __name__ == "__main__":
    main()