import json
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread
from PIL import Image, ImageDraw
import cv2

def polygons_to_mask_array(polygons, width : int = 300, height : int = 300) -> np.ndarray:
    img = Image.new('L', (width, height), 0)
    for polygon in polygons:
        nested_lst_of_tuples = [tuple(l) for l in polygon['points']]
        ImageDraw.Draw(img).polygon(nested_lst_of_tuples, outline=1, fill=1)
    mask = np.array(img)

    return mask

cpt = 0
moy = 0

print("Beginning of the test ...")

for j in range (1,52):
    im2 = imread('Test + Traitement/'+str(j)+'.jpg')
    img = cv2.resize(im2, (500, 500))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v= cv2.split(hsv)

    with open('Test + Traitement/'+str(j)+'.json', "r", encoding = 'utf-8') as f:
            data = json.load(f)
    fileObject = open('Test + Traitement/'+str(j)+'.json', 'r')
    jsonContent = fileObject.read()
    obj_python = json.loads(jsonContent)
    test = obj_python["shapes"]

    ret_h, L = cv2.threshold(s,0,255,cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    kernelBis = np.ones((3, 3), np.uint8)
    L = cv2.erode(L, kernel)
    L = cv2.dilate(L, kernel)
    L = cv2.medianBlur(L, 5)
    L = cv2.medianBlur(L, 9)

    maskBin = polygons_to_mask_array(data['shapes'], im2.shape[1], im2.shape[0])
    maskBin = cv2.resize(maskBin, (500,500))

    pixImg = np.where(L == 255)
    pixMask = np.where(maskBin == 1)
    pixMoy = len(pixImg[1]) / len(pixMask[1])
    if(pixMoy > 1):
        pixMoy = len(pixMask[1]) / len(pixImg[1])
    moy += pixMoy
    

print("We managed to binarize the image at a rate of "+ str((moy/51)*100)+"%")