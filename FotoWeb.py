#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 22:10:13 2020

@author: alejandro
"""
import cv2
import json
import sqlite3
from datetime import datetime
from watson_developer_cloud import VisualRecognitionV3

cap = cv2.VideoCapture(0)

leido, frame = cap.read()

if leido == True:
    rutaImagen = '/home/alejandro/Escritorio/Hackaton/foto.png'
    cv2.imwrite(rutaImagen,frame)
    print("Foto tomada correctamente")
else:
	print("Error al acceder a la cámara")

cap.release()

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='b5i2lf-LJkzRlUAbxTGlM-k_uokxL9dD8FRYXX48Y-iD')

with open(rutaImagen, 'rb') as images_file:
    classes = visual_recognition.classify(
        images_file,
        threshold='0.6',
 	classifier_ids='Cubrebocas_1266465768').get_result()
to_json = json.dumps(classes, indent=2) 
print(to_json)

to_python = json.loads(to_json)
aux = to_python.get('images')
aux[0].get('classifiers')
aux1 = aux[0].get('classifiers')
clases = aux1[0].get('classes')
cl = []
sc = []
for clase in clases:
    cl.append(clase.get('class'))
    sc.append(float(clase.get('score')))
ind = sc.index(max(sc))
if cl[ind] == 'Nocubrebocas':
    print("Persona no esta usando cubrebocas")
    print("Sonar alarma")
    conn = sqlite3.connect('/home/alejandro/Escritorio/Hackaton/registros.db')
    
    cur = conn.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS Registros(fecha text,foto blob)")
    conn.commit()
    
    cur.execute("INSERT INTO Registros(fecha,foto) VALUES(?,?)",(datetime.now(),rutaImagen))
    conn.commit()
    
    conn.close()
    print("Imagen guardada en Base-Registros")
    
else:
    print("Foto cumple los requerimientos ")

