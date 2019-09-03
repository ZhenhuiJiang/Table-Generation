"""
For image padding to square
"""


import os
import cv2

def padding_img(image):
    img = cv2.imread(image)
    shape = max(img.shape)
    high = img.shape[0]
    length = img.shape[1]
    top = int((shape - high) / 2)
    bottom = shape - high - top
    left = int((shape - length) / 2)
    right = shape - length - left
    newimg = cv2.copyMakeBorder(
    img,
    top, bottom, left, right, cv2.BORDER_CONSTANT,
    value=[
        255,
        255,
        255])
    return newimg

# image_location='./train_image/'
# output_location='./pad_train_image/'

image_location='./train_image/'
output_location='./pad_train_image/'

for _, dirs, files in os.walk(image_location):
    for file in files:
        if file.endswith('.png'):
            # print(file)
            newimg=padding_img(image_location+file)
            cv2.imwrite(output_location+f'pad_{file}', newimg)

