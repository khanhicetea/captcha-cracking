import os
import glob
import cv2


def preprocess_img(filename):
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    dilation = cv2.dilate(img,kernel,iterations = 1)
    ret, thresh1 = cv2.threshold(dilation, 127, 255,cv2.THRESH_BINARY)
    substracted_img = cv2.subtract(thresh1, dilation)
    result_img = cv2.bitwise_not(substracted_img)
    return result_img

for filename in glob.glob('data/*.png'):
    save_to = filename.replace('data/', 'processed/')
    if not os.path.exists(save_to):
        img = preprocess_img(filename)
        cv2.imwrite(save_to, img)
        print("- Processed {}".format(filename))

