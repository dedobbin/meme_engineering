from tumblr import tumblr
from automatic_watermarker import automatic_watermarker
import cv2
import numpy as np
from random import choice
from string import ascii_uppercase
import os

def main():
    imgs = tumblr.get_image_from_profile("sweetoothgirl", n = 1)
    if not os.path.exists("output"):
        os.mkdir("output")
    
    for img in imgs:
        watermark_name = "./automatic_watermarker/Trollface.png"
        energy = automatic_watermarker.forward_energy(img)
        cv2.imwrite("Features.jpg", energy)

        zone = automatic_watermarker.findDark(energy)
        finalImage = automatic_watermarker.addWatermark(zone, img,watermark_name)
        cv2.imwrite(str(os.getcwd()) + "/output/%s" % ''.join(choice(ascii_uppercase) for i in range(12)) + ".png", finalImage)


if __name__ == "__main__":
    main()