
import os
import cv2

def dilation(image,thre=-1):
    img = cv2.imread(image)
    mean = img.mean()
    std = img.std()
    #     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if thre <= -1:
        ret, thresh1 = cv2.threshold(img, mean - std, 255, cv2.THRESH_BINARY_INV)
    else:
        ret, thresh1 = cv2.threshold(img, thre, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))  # 椭圆结构
    dilation = cv2.dilate(thresh1, kernel)  # 膨胀
    # kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 定义结构元素
    # closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel2)  # 闭运算
    closing = cv2.blur(dilation, (7, 7))  # 平滑
    return closing

# image_location='./pad_train_image/'
# output_location='./dilation_train/'

image_location='./pad_train_image/'
output_location='./dilation_train/'

for _, dirs, files in os.walk(image_location):
    for file in files:
        if file.endswith('.png'):
            # print(file)
            newimg=dilation(image_location+file)
            cv2.imwrite(output_location+f'dilation_{file}', newimg)

