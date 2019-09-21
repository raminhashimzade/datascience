#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 22:53:49 2019

conda create -n py37 python=3.7
activate py36

conda config --add channels conda-forge
conda install numpy
conda install scipy
conda install dlib

pip install --no-dependencies face_recognition

@author: ramin
"""

def checkFaceEncoding(unknown_encoding):
    if len(unknown_encoding) > 0:
        print("faces found in the image!")
        return 1
    else:
       print("No faces found in the image!")
       return 0
    
import face_recognition

img1 = "/home/ramin/git/datascience/faceVerification/images/2.jpg"
img2 = "/home/ramin/git/datascience/faceVerification/images/L2.jpg"

known_image = face_recognition.load_image_file(img1)
unknown_image = face_recognition.load_image_file(img2)

known_encoding = face_recognition.api.face_encodings(known_image)
unknown_encoding = face_recognition.api.face_encodings(unknown_image)


if (checkFaceEncoding(known_encoding) == 0):
    exit()

if (checkFaceEncoding(unknown_encoding) == 0):
    exit()
    
known_encoding = known_encoding[0]
unknown_encoding = unknown_encoding[0]
    

results = face_recognition.api.compare_faces([known_encoding], unknown_encoding)
print(results)
dis = face_recognition.api.face_distance([known_encoding], unknown_encoding)
print(dis)
