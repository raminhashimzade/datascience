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
   
    
import numpy as np    
import face_recognition
from PIL import Image, ImageDraw
from IPython.display import display

img1 = "/home/ramin/git/datascience/faceVerification/images/L1.jpg"
img2 = "/home/ramin/git/datascience/faceVerification/images/L2.jpg"

known_image = face_recognition.load_image_file(img1)
unknown_image = face_recognition.load_image_file(img2)

known_encoding = face_recognition.api.face_encodings(known_image)[0]
unknown_encoding = face_recognition.api.face_encodings(unknown_image)


known_face_encodings = [
    known_encoding
]
known_face_names = [
    "Target Person"
]

##############################


# Find all the faces and face encodings in the unknown image
face_locations = face_recognition.face_locations(unknown_image)
face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

# Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
# See http://pillow.readthedocs.io/ for more about PIL/Pillow
pil_image = Image.fromarray(unknown_image)
# Create a Pillow ImageDraw Draw instance to draw with
draw = ImageDraw.Draw(pil_image)

# Loop through each face found in the unknown image
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    # See if the face is a match for the known face(s)
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    name = "Unknown"
    
    # Or instead, use the known face with the smallest distance to the new face
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face_names[best_match_index]
        
    # Draw a box around the face using the Pillow module
    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

    # Draw a label with a name below the face
    text_width, text_height = draw.textsize(name)
    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
    draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

# Remove the drawing library from memory as per the Pillow docs
del draw

# Display the resulting image
display(pil_image)
