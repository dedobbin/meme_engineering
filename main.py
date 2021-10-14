from tumblr import tumblr
from automatic_watermarker import automatic_watermarker
import cv2
import numpy as np
from random import choice
from string import ascii_uppercase
import os
from glob import glob as find_file_names

def main():
    imgs = tumblr.get_image_from_profile("sweetoothgirl", n = 10)
    if not os.path.exists("output"):
        os.mkdir("output")
    
    watermark_list= find_file_names("./automatic_watermarker/watermarks/*.png")

    for img in imgs:
        watermark_name = choice(watermark_list)
        energy = automatic_watermarker.forward_energy(img)
        #cv2.imwrite("Features.jpg", energy)
        zone = automatic_watermarker.findDark(energy)
        finalImage = automatic_watermarker.addWatermark(zone, img,watermark_name)
        cv2.imwrite(str(os.getcwd()) + "/output/%s" % ''.join(choice(ascii_uppercase) for i in range(12)) + ".png", finalImage)


if __name__ == "__main__":
    main()