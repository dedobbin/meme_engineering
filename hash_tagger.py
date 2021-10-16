import cv2
from hashlib import sha256
from automatic_watermarker import automatic_watermarker
from cv2 import putText, FONT_HERSHEY_DUPLEX
import logging

def tag_image(image):
    img_hash = str(sha256(image).hexdigest())[:16]
    tagged_img = hash_tag_image(image, img_hash)
    return tagged_img

def hash_tag_image(image, hash):
    feature_map = automatic_watermarker.forward_energy(image)
    tag_coord = automatic_watermarker.findDark(feature_map)
    scale = 1
    logging.info("adding hash: " + hash)
    font_size = min(image.shape[0], image.shape[1])/(1000/scale)
    thickness = 1

    (font_w, font_h), _ = cv2.getTextSize(hash[:8], FONT_HERSHEY_DUPLEX, font_size, thickness+2)

    img_h, img_w = image.shape[:2]

    tag_y, tag_x = tag_coord

    #this manages oob, it can be really fucky, i hate python tuples
    #also there are probably much more elegant ways to handle this
    while tag_y < 0 or tag_y - (2* font_h) < 0 or tag_x < 0 or tag_x > img_w - font_w:

        if(tag_y < 0):
            tag_y = 0
        
        if(tag_x < 0):
            tag_x = 0

        if(tag_y - (2* font_h) < 0):
            tag_y = 0 + (2 * font_h)

        if(tag_x > img_w - font_w):
            tag_x = img_w - font_w
            


    putText(image, hash[:8], (tag_x, tag_y), FONT_HERSHEY_DUPLEX, font_size, (0,0,0), thickness+2)
    putText(image, hash[8:], (tag_x, tag_y+font_h), FONT_HERSHEY_DUPLEX, font_size, (0,0,0), thickness+2)

    putText(image, hash[:8], (tag_x, tag_y), FONT_HERSHEY_DUPLEX, font_size, (255,255,255), thickness)
    putText(image, hash[8:], (tag_x, tag_y+font_h), FONT_HERSHEY_DUPLEX, font_size, (255,255,255), thickness)
    return image