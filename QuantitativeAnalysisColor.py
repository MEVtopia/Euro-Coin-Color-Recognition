import json
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from PIL import Image, ImageDraw
from pathlib import Path
from time import time
import cv2
from skimage.measure import label


cptFail = 0

def polygons_to_mask_array(polygons, width : int = 300, height : int = 300) -> np.ndarray:
    img = Image.new('L', (width, height), 0)
    for polygon in polygons:
        nested_lst_of_tuples = [tuple(l) for l in polygon['points']]
        ImageDraw.Draw(img).polygon(nested_lst_of_tuples, outline=1, fill=1)
    mask = np.array(img)

    return mask

cptCouleur = 0
nbPieceTotal = 0
nbPieceTrouve = 0
for o in range(1,52):

    print("Image : "+str(o))
    im2 = imread('Test + Traitement/'+str(o)+'.jpg')
    img = cv2.resize(im2, (500, 500))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v= cv2.split(hsv)

    with open('Test + Traitement/'+str(o)+'.json', "r", encoding = 'utf-8') as f:
            data = json.load(f)
    fileObject = open('Test + Traitement/'+str(o)+'.json', 'r')
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

    a = label(L,background=0,return_num=False,connectivity=2)
    b = label(L,background=0,return_num=True,connectivity=2)

    l = []

    plt.subplot(2,2,2)
    plt.imshow(L)

    listeCouleur = []
    listePoints = []  #Le tableau sera de la forme ((haut,bas,gauche,droite),(haut,bas,gauche,droite)), etc
    listeCouleurPoints = []
    nbPieceTotal += b[1]

    for k in range (1,b[1]+1) :
        basb = True
        hautb = True
        gaucheb = True
        droiteb = True
        listeTmp = [None] * 4
        listeTmpCouleurs = []
        for i in range(500):
            for j in range (500):
                if (a[i][j] == k ) :
                    listeCouleur.append((i,j))
                    listeTmpCouleurs.append((i,j))  
                if (a[i][j] == k and hautb) :
                    haut = [i,j]
                    listeTmp[0] = haut
                    hautb = False
                elif (a[j][i] == k and gaucheb) :
                    gauche = [i,j]
                    listeTmp[2] = gauche
                    gaucheb = False
                elif(a[499-i][499-j] == k and basb) :
                    bas = [499 - i,499 - j]
                    listeTmp[1] = bas
                    basb = False
                elif(a[499 - j][499 - i] == k and droiteb) :
                    droite = [499 -i, 499 - j]
                    listeTmp[3] = droite
                    droiteb = False
        listeCouleurPoints.append(listeTmpCouleurs)
        listePoints.append(listeTmp) 

    moyenne = [0, 0, 0]
    moyennePieces = [[0,0,0] for i in range(b[1])]

    moyenneHSV = [[0,0,0] for i in range(b[1])]

    for k in range (b[1]) :
        for i in listeCouleurPoints[k] :
            for j in range(3) :
                moyennePieces[k][j] += (img[i])[j]
                moyenneHSV[k][j] +=  (hsv[i])[j]
            
            
        moyennePieces[k][0] = moyennePieces[k][0] / len(listeCouleurPoints[k])
        moyennePieces[k][1] = moyennePieces[k][1] / len(listeCouleurPoints[k])
        moyennePieces[k][2] = moyennePieces[k][2] / len(listeCouleurPoints[k])
        moyenneHSV[k][0] = moyenneHSV[k][0] / len(listeCouleurPoints[k])
        moyenneHSV[k][1] = moyenneHSV[k][1] / len(listeCouleurPoints[k])
        moyenneHSV[k][2] = moyenneHSV[k][2] / len(listeCouleurPoints[k])

    milieuu = []

    for i in range (b[1]) :
        milieuu.append([int((listePoints[i][3][0] + listePoints[i][2][0])/2),int((listePoints[i][1][0] + listePoints[i][0][0])/2)])

    milieu = [int((droite[0] + gauche[0])/2),int((bas[0] + haut[0])/2)]

    recupValeurPiece = {}
    for k in range (b[1]) :
        if (moyenneHSV[k][2] > 0 and moyenneHSV[k][2] < 50) :
            if (moyenneHSV[k][0] >= 109 and moyenneHSV[k][0] < 118) :
                recupValeurPiece["Piece " + str(k+1)] = "Rouge"
            elif(moyenneHSV[k][0] >= 97 and moyenneHSV[k][0] < 104) :
                recupValeurPiece["Piece " + str(k+1)] = "Jaune"
            elif (moyenneHSV[k][0] >= 104 and moyenneHSV[k][0] < 105) :
                recupValeurPiece["Piece " + str(k+1)] = "2Euro"
            elif (moyenneHSV[k][0] >= 105 and moyenneHSV[k][0] < 109) :
                recupValeurPiece["Piece " + str(k+1)] = "1Euro"
            else :
                recupValeurPiece["Piece " + str(k+1)] = "Inconnu"
        
        elif(moyenneHSV[k][2] >= 50 and moyenneHSV[k][2] < 70) :
            if (moyenneHSV[k][0] >= 109 and moyenneHSV[k][0] < 118) :
                recupValeurPiece["Piece " + str(k+1)] = "Rouge"
            elif(moyenneHSV[k][0] >= 97 and moyenneHSV[k][0] < 104) :
                recupValeurPiece["Piece " + str(k+1)] = "Jaune"
            elif (moyenneHSV[k][0] >= 104 and moyenneHSV[k][0] < 105) : 
                recupValeurPiece["Piece " + str(k+1)] = "2Euro"
            elif (moyenneHSV[k][0] >= 104 and moyenneHSV[k][0] < 109) : 
                recupValeurPiece["Piece " + str(k+1)] = "1Euro"
            else :
                recupValeurPiece["Piece " + str(k+1)] = "Inconnu"
        
        elif(moyenneHSV[k][2] >= 70 and moyenneHSV[k][2] < 90) :
            if (moyenneHSV[k][0] >= 109 and moyenneHSV[k][0] < 118) :
                recupValeurPiece["Piece " + str(k+1)] = "Rouge"
            elif(moyenneHSV[k][0] >= 97 and moyenneHSV[k][0] < 104) :
                recupValeurPiece["Piece " + str(k+1)] = "Jaune"
            elif (moyenneHSV[k][0] >= 104 and moyenneHSV[k][0] < 109) :
                recupValeurPiece["Piece " + str(k+1)] = "1Euro"
            else :
                recupValeurPiece["Piece " + str(k+1)] = "Inconnu"

        elif(moyenneHSV[k][2] >= 90 and moyenneHSV[k][2] < 110) :
            
            if (moyenneHSV[k][0] >= 105 and moyenneHSV[k][0] < 140) :
                recupValeurPiece["Piece " + str(k+1)] = "Rouge"
            elif(moyenneHSV[k][0] >= 95 and moyenneHSV[k][0] < 104) :
                recupValeurPiece["Piece " + str(k+1)] = "Jaune"
            elif (moyenneHSV[k][0] >= 104 and moyenneHSV[k][0] < 105) :
                recupValeurPiece["Piece " + str(k+1)] = "1Euro"
            else :
                recupValeurPiece["Piece " + str(k+1)] = "Inconnu"

        elif(moyenneHSV[k][2] >= 110 and moyenneHSV[k][2] < 255) :
            if (moyenneHSV[k][0] >= 105 and moyenneHSV[k][0] < 140) :
                recupValeurPiece["Piece " + str(k+1)] = "Rouge"
            elif(moyenneHSV[k][0] >= 90 and moyenneHSV[k][0] < 103.9) :
                recupValeurPiece["Piece " + str(k+1)] = "Jaune"
            elif (moyenneHSV[k][0] >= 103.9 and moyenneHSV[k][0] < 105) :
                recupValeurPiece["Piece " + str(k+1)] = "1Euro"
            else :
                recupValeurPiece["Piece " + str(k+1)] = "Inconnu"


    nbPieceRouge = 0
    nbPieceJaune = 0
    nbPiece1e = 0
    nbPiece2e = 0
    

    for i in range (len(test)):
        if ( test[i]['label'] == '1c' or test[i]['label'] == '2c' or test[i]['label'] == '5c'):
            nbPieceRouge += 1
        elif ( test[i]['label'] == '10c' or test[i]['label'] == '20c' or test[i]['label'] == '50c'):
            nbPieceJaune += 1
        elif ( test[i]['label'] == '1e'):
            nbPiece1e += 1
        else :
            nbPiece2e += 1

    cptTr = 0

    for piece, couleur in recupValeurPiece.items() :
        if(nbPieceRouge != 0 and couleur == 'Rouge'):
            nbPieceRouge -= 1
            nbPieceTrouve += 1
            cptTr +=1 
        elif(nbPieceJaune != 0 and couleur == 'Jaune'):
            nbPieceJaune -= 1
            nbPieceTrouve += 1
            cptTr +=1 
        elif(nbPiece1e != 0 and couleur == '1Euro'):
            nbPiece1e -= 1
            nbPieceTrouve += 1
            cptTr +=1 
        elif(nbPiece2e != 0 and couleur == '2Euro'):
            nbPiece2e -= 1
            nbPieceTrouve += 1
            cptTr +=1 
        else:
            cptFail += 1
            
    print("We found "+str(cptTr)+" color(s), on a total of "+str(b[1])+" color(s)")

print("We found at "+str((nbPieceTrouve/nbPieceTotal)*100)+"% the correct color")
