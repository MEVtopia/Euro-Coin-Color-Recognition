import numpy as np
import matplotlib.pyplot as plt
from skimage import feature,color,filters, morphology
from skimage.io import imread, imsave
from skimage.measure import label
import cv2

#Initialisation de plusieurs variables qui sont utilisées
listePoints = []  
listeCouleurPoints = []
milieu = []
recupValeurPiece = {}
sumMin = 0
sumMax = 0
sumMid = 0

#Appel de l'image a tester
im2 = imread('Test + Traitement/14.jpg')

#Application de plusieurs filtres pour créer l'image binarisée
img = cv2.resize(im2, (500, 500))
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v= cv2.split(hsv)
ret_h, L = cv2.threshold(s,0,255,cv2.THRESH_OTSU)
kernel = np.ones((5, 5), np.uint8)
kernelBis = np.ones((3, 3), np.uint8)
L = cv2.erode(L, kernel)
L = cv2.dilate(L, kernel)
L = cv2.medianBlur(L, 5)
L = cv2.medianBlur(L, 9)

#On appelle 2 labels pour faciliter la manipulation de l'image sous forme de tableau                                            
a = label(L,background=0,return_num=False,connectivity=2)
b = label(L,background=0,return_num=True,connectivity=2)

#On cherche les 4 extrémitées d'une pièce pour rogner la pièce et on récupère les coordonnées des points de chaque pièce
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
                listeTmpCouleurs.append((i,j)) # On sauvegarde chaque pixel d'une pièce
            if (a[i][j] == k and hautb) : # On trouve le haut de la pièce
                haut = [i,j]
                listeTmp[0] = haut
                hautb = False
            elif (a[j][i] == k and gaucheb) : # On trouve la gauche de la pièce
                gauche = [i,j]
                listeTmp[2] = gauche
                gaucheb = False
            elif(a[499-i][499-j] == k and basb) : # On trouve le bas de la pièce
                bas = [499 - i,499 - j]
                listeTmp[1] = bas
                basb = False
            elif(a[499 - j][499 - i] == k and droiteb) : # On trouve la droite de la pièce
                droite = [499 -i, 499 - j]
                listeTmp[3] = droite
                droiteb = False
    listeCouleurPoints.append(listeTmpCouleurs)
    listePoints.append(listeTmp) 

plt.imshow(L, cmap="gray")
plt.show()

#Initialisation des moyennes RGB et HSV
moyennePieces = [[0,0,0] for i in range(b[1])]
moyenneHSV = [[0,0,0] for i in range(b[1])]


#On calcule la moyenne RGB et HSV de chaque pièce
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
    
    
#Affichage de la moyenne HSV
print("HSV moyenne ci-dessous : ")
print(moyenneHSV)


for i in range (b[1]) :
    milieu.append([int((listePoints[i][3][0] + listePoints[i][2][0])/2),int((listePoints[i][1][0] + listePoints[i][0][0])/2)])


print(moyennePieces)

#Comparaison des valeurs trouvées par le filtre HSV pour chaque pièce afin de déterminer sa valeur.
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

#Affichage du dictionnaire
print(recupValeurPiece)

#Calcul de la valeur en Euros/Centimes de l'image.
for i in recupValeurPiece.values() :
    if (i == "Jaune") :
        sumMin += 0.1
        sumMid += 0.266
        sumMax += 0.5
    elif (str(i) == "Rouge") :
        sumMin += 0.01
        sumMid += 0.026
        sumMax += 0.05
    elif (str(i) == "1Euro") :
        sumMin += 1
        sumMax += 1
        sumMid += 1

#Affichage  de la  valeur en Euros/Centimes de la pièce trouvé par notre script, et estimation de cette valeur.
print("It seems that there is on this image at least " + str(sumMin) + " euros.")
print("On average, there is " + str(sumMid) + " euros, and at maximum " + str(sumMax) + " euros.")

imgfullText = np.copy(img) # Pour écrire le numéro de chaque pièce et comparer ensuite avec le dictionnaire recupValeurPiece

tabPieces = []
for valeur in recupValeurPiece.values() :
    tabPieces.append(valeur)

#Ecriture du numéro de la pièce au centre de celle-ci sur l'image traitée.
for i in range (1,b[1] + 1) :
    plt.subplot(2,2,((i-1)%4)+1)
    plt.imshow(L[listePoints[i-1][0][0]:listePoints[i-1][1][0], listePoints[i-1][2][0]:listePoints[i-1][3][0]], cmap = plt.cm.gray)
    if (i%4 == 0 or i == b[1]) :
        plt.show()

for i in range (1,b[1] + 1) :
    imgfullText = cv2.putText(img=imgfullText, text="Piece " + tabPieces[i-1], 
    org=(milieu[i-1][0] -30,milieu[i-1][1]),fontFace=1, fontScale=1, color=(0,255,0), thickness=2)
    cv2.putText(img=imgfullText, text= "", org=(30,30),fontFace=2, fontScale=1, color=(0,255,0), thickness=1)


#Affichage de l'image sous filtre HSV
plt.imshow(hsv)
plt.show()

#Affichage de l'image global avec la numérotation des pièces
plt.imshow(imgfullText)
plt.show()