# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 20:47:26 2023

@author: dongmo
"""



import cv2
import os
import numpy as np
import pandas as pd
from pandas import ExcelWriter
from openpyxl import Workbook
from openpyxl import load_workbook 
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import Label, Entry, Button, StringVar
import time
from tkinter import filedialog



#import openpyxl

fps = 0.30

# Définir la variable points_selectionnes au niveau du module pour la garder en mémoire
points_selectionnes = []


# Définir le chemin de base vers le répertoire des images

# Chemin d'accès vers la video

Chemin_video = r'C:\Users\dongm\Desktop\TEST1_Resize.avi'
video = cv2.VideoCapture(Chemin_video)

# Charger l'image de référence et copier pour affichage

ret, reference_image = video.read()

if reference_image is None:
    print("L'image n'a pas pu être lue. Assurez-vous que le chemin est correct.")
else:
    print("L'image a été lue avec succès.") 
    
#gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)  # Convertir en niveaux de gris (to_delete)
image_affichage = reference_image #.copy()

# convertir en niveaux de gris
gray_ref = cv2.cvtColor(image_affichage, cv2.COLOR_BGR2GRAY) 

#Lucas Kanade params
lk_params = dict(winSize=(50, 50), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 500, 0.0001)) 

# # params for ShiTomasi corner detection
# feature_params = dict( maxCorners = 100,
#  qualityLevel = 0.3,
#  minDistance = 7,
#  blockSize = 7 )

# Create some random colors
color = np.random.randint(0, 255, (100, 3))


print('KINDLY SELECT TWO POINTS IN THE IMAGE')
print()
print('THE COORDINATES OF THE TWO POINTS ARE: ')


# Définir la fonction de rappel pour la souris

# def click_callback(event, x, y, flags, param):
#     # Utiliser la variable points_selectionnes définie en dehors de cette fonction
#     global points_selectionnes

#     # Récupérer les coordonnées des points sélectionnés par l'utilisateur
#     if event == cv2.EVENT_LBUTTONDOWN:
#         if len(points_selectionnes) == 2:
#             print("Now press the enter button to continue...")
#         else:
#             points_selectionnes.append((x, y))
#             print("Clic détecté ! Coordonnées : (", x, ",", y, ")")


def click_callback(event, x, y, flags, param):
    # Utiliser la variable points_selectionnes définie en dehors de cette fonction
    global points_selectionnes

    # Récupérer les coordonnées des points sélectionnés par l'utilisateur
    if event == cv2.EVENT_LBUTTONDOWN and len(points_selectionnes) < 2:
        points_selectionnes.append((x, y))
        print("Clic détecté ! Coordonnées : (", x, ",", y, ")")
        if len(points_selectionnes) == 2:
          show_xy_edit_dialog()
          print("Now press the enter button to continue...")

#Create a dialog window
        
def show_xy_edit_dialog():
  global points_selectionnes
  dialog = tk.Tk()
  dialog.title('Edit Points')

  point1_label = Label(dialog, text='Point 1:')
  point1_label.grid(row=0, column=0)
  point2_label = Label(dialog, text='Point 2:')
  point2_label.grid(row=1, column=0)

  point1_x_var = StringVar()
  point1_y_var = StringVar()
  point2_x_var = StringVar()
  point2_y_var = StringVar()

  point1_x_var.set(str(points_selectionnes[0][0]))
  point1_y_var.set(str(points_selectionnes[0][1]))
  point2_x_var.set(str(points_selectionnes[1][0]))
  point2_y_var.set(str(points_selectionnes[1][1]))

  point1_x_entry = Entry(dialog, textvariable=point1_x_var)
  point1_y_entry = Entry(dialog, textvariable=point1_y_var)
  point2_x_entry = Entry(dialog, textvariable=point2_x_var)
  point2_y_entry = Entry(dialog, textvariable=point2_y_var)

  point1_x_entry.grid(row=0, column=1)
  point1_y_entry.grid(row=0, column=2)
  point2_x_entry.grid(row=1, column=1)
  point2_y_entry.grid(row=1, column=2)

  def update_points():
      points_selectionnes[0] = (int(point1_x_var.get()), int(point1_y_var.get()))
      points_selectionnes[1] = (int(point2_x_var.get()), int(point2_y_var.get()))
      # dialog.destroy()
      print(f"les nouveaux points spécifiés;   point1: {points_selectionnes[0]} \n\r point2: {points_selectionnes[1]}")
      for point in points_selectionnes: 
        cv2.circle(image_affichage, point,2, (0, 0, 255), -1)
        cv2.line(image_affichage, (point[0], 0), (point[0], image_affichage.shape[0]), (189,252,201), 1) #Vertical line
      cv2.imshow('Image de traction', image_affichage) 
      
  update_button = Button(dialog, text='Update', command=update_points)
  update_button.grid(row=2, column=0, columnspan=3)
  dialog.mainloop()

#print(points_selectionnes)

# Créer une fenêtre graphique pour l'interaction avec l'utilisateur
cv2.namedWindow('Image de traction')
cv2.setMouseCallback('Image de traction', click_callback)



while True:
    for point in points_selectionnes: 
        cv2.circle(image_affichage, point,2, (0, 0, 255), -1)
        #cv2.line(image_affichage, (point[0], 0), (point[0], image_affichage.shape[0]), (189,252,201), 1) #Vertical line
    cv2.imshow('Image de traction', image_affichage) 
    
    key = cv2.waitKey(1)
    if key == 13: # Touche Entrée
        break
    

#points_selectionnes = cv2.goodFeaturesToTrack(gray_ref, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(image_affichage)

# Liste pour stocker les déformations en fonction du nombre d'images
deformations_temps = []

# Create some random colors
color = np.random.randint(0, 255, (100, 3))

# Convertir les points sélectionnés en format numpy

points_ref = np.array(points_selectionnes, dtype=np.float32).reshape(-1, 1, 2)

#Calcul distance entre les points de references

converted_ref = np.array(points_ref, dtype=object)
distance_ref = np.sqrt((converted_ref[1][0][0] - converted_ref[0][0][0] )**2 + (converted_ref[1][0][1]  - converted_ref[0][0][1] )**2)

#gray_ref = cv2.cvtColor(image_affichage, cv2.COLOR_BGR2GRAY) # convertir en niveaux de gris


# Intialisation de la frame de la video 
frame_number = 1


# Create a mask image for drawing purposes
mask = np.zeros_like(image_affichage)

# Boucle pour suivre l'essai de traction à partir des frames

while True:  
    
    ret, frame = video.read()    
    if ret == True:
        frame_number +=1
        
        print('INTERATION NO: ', frame_number) 
         
        image_courante = frame 
        gray_img = cv2.cvtColor(image_courante, cv2.COLOR_BGR2GRAY) # convertir en niveaux de gris
        
        #you can change the speed of the frame per seconde 
        if frame_number % 1 == 0:
            
            # Calculer le déplacement des points d'intérêt entre l'image de référence et l'image courante
            points_img, st, _ = cv2.calcOpticalFlowPyrLK(gray_ref, gray_img, points_ref, None, **lk_params)
            
            # Select good points
            if points_img is not None:
                   good_new = points_img[st==1]
                   good_old = points_ref[st==1]
                   
                   if len(good_new) >=2:
                        # draw the tracks
                        for i, (new, old) in enumerate(zip(good_new, good_old)):
                            a, b = new.ravel()
                            c, d = old.ravel()
                            mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
                            frame = cv2.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)
                        img = cv2.add(frame, mask)
                        
                       
                        
                        # # Now update the previous frame and previous points
                        # gray_ref = gray_img.copy()
                        # points_ref = good_new.reshape(-1, 1, 2)
                        
                        # Calculer la déformation relative entre les points d'intérêt
                     
                        deformations = []
                        #converted_ref = np.array(points_ref, dtype=object)
                        converted_img = np.array(points_img, dtype=object)
                        
                        #print(converted_img[0][0],converted_img[1][0],converted_img[0][0][0],converted_img[1][0][0],converted_img[0][0][1],converted_img[1][0][1])
                        
                        #distance_ref = np.sqrt((converted_ref[1][0][0] - converted_ref[0][0][0] )**2 + (converted_ref[1][0][1]  - converted_ref[0][0][1] )**2)
                        
                        distance_img = np.sqrt((converted_img[1][0][0] - converted_img[0][0][0] )**2 + (converted_img[1][0][1]  - converted_img[0][0][1] )**2)
                        
                        delta_L = distance_img - distance_ref
                        
                        deformations = delta_L/distance_ref
                        
                        for point in (list(map(round,converted_img[0][0])),list(map(round,converted_img[1][0]))):
                            cv2.circle(image_courante, point,2, (0, 0, 255), -1)
                            cv2.line(image_courante, (point[0], 0), (point[0], image_courante.shape[0]), (189,252,201), 1) #Vertical line
                    
                        
                        print('DISTANCE POINTS REFERENCE: ', distance_ref)
                        print('DISTANCE POINTS IMAGE PRESENTE: ', distance_img)
                        print('lENGTH VARIATION: ', delta_L)
                        print('DEFORMATION VALUE: ', deformations)
                        
                        deformations_temps.append(deformations)
                        
                        # # Now update the previous frame and previous points
                        # gray_ref = gray_img.copy()
                        # points_ref = good_new.reshape(-1, 1, 2)
                        
                        # Ajoutez le numéro de frame en haut à gauche de l'image
                        
                        cv2.putText(img, f'Deformation: {deformations:.6f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) 
                        cv2.putText(img, f'Frame_number: {frame_number}' , (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        #cv2.imshow('Image de traction', image_courante)
                        cv2.imshow('Image de traction', img)
                        cv2.waitKey(int(fps*1000))
                        
                        # Now update the previous frame and previous points
                        gray_ref = gray_img.copy()
                        points_ref = good_new.reshape(-1, 1, 2)
                        
                   else:
                      # Ajoutez des logs ou des messages d'erreur pour le débogage
                      print("Pas assez de points valides pour le suivi.")
            else:
                # Ajoutez des logs ou des messages d'erreur pour le débogage
                print("Erreur dans le calcul du flux optique. points_img est None.")    
                                 
    else:
        break

    
video.release()
cv2.destroyAllWindows()

fichier_excel = 'deformations.xlsx'

# Créer un nouveau fichier Excel avec les données de déformation
frame_numbers = [i * 1 for i in range(1, len(deformations_temps) + 1)]
data = pd.DataFrame({'Frame_number': frame_numbers, 'Deformation': deformations_temps})
data.to_excel(fichier_excel, index=False)


print('New fichier_Excel created')

 
 # Afficher les déformations en fonction du temps 
frame_numbers = [i * 1 for i in range(1, len(deformations_temps) + 1)]
plt.plot(frame_numbers, deformations_temps, label="Original curve")

plt.xlabel('Image')
plt.ylabel('Déformation')
plt.title("Déformation du spécimen en fonction du nombre d'image")
plt.legend()
plt.show()

print(f'la distance de référence est: {distance_ref}')



