import json
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
from pathlib import Path
import cv2
from skimage.measure import label

def polygons_to_mask_array(polygons, width : int = 300, height : int = 300) -> np.ndarray:
    img = Image.new('L', (width, height), 0)
    for polygon in polygons:
        nested_lst_of_tuples = [tuple(l) for l in polygon['points']]
        ImageDraw.Draw(img).polygon(nested_lst_of_tuples, outline=1, fill=1)
    mask = np.array(img)

    return mask

cpt = 0

for j in range(1,52):
    
    im2 = cv2.imread('Test + Traitement/'+str(j)+'.jpg')
    im3 = cv2.resize(im2, (500, 500))
    hsv = cv2.cvtColor(im3, cv2.COLOR_BGR2HSV)
    h,s,v= cv2.split(hsv)

    with open('Test + Traitement/'+str(j)+'.json', "r", encoding = 'utf-8') as f:
        data = json.load(f)

    fileObject = open('Test + Traitement/'+str(j)+'.json', 'r')
    jsonContent = fileObject.read()
    obj_python = json.loads(jsonContent)
    test = obj_python["shapes"]

    maskBin = polygons_to_mask_array(data['shapes'], im2.shape[1], im2.shape[0])


    ret_h, L = cv2.threshold(s,0,255,cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    kernelBis = np.ones((3, 3), np.uint8)
    L = cv2.erode(L, kernel)
    L = cv2.dilate(L, kernel)
    L = cv2.medianBlur(L, 5)
    L = cv2.medianBlur(L, 9)

    bBis = label(L,background=0,return_num=True,connectivity=2)
    nbPiece = bBis[1]

    a = label(maskBin,background=0,return_num=True,connectivity=2)

    print("Image "+ str(j) + " : \n Label fichier PNG  : " + str(nbPiece))
    print("Label fichier JSON : " + str(a[1]))

    if(a[1] == nbPiece):
        cpt += 1

print("We found at "+str((cpt/51)*100)+"% the correct number fo coins")