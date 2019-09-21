#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 14:39:01 2019

@author: ramin
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 22:53:49 2019

conda create -n py37 python=3.7
activate py36
conda config --add channels conda-forge


if  centos
   sudo yum install python36-devel  or sudo yum install python36u-devel


pip install cmake
pip install numpy
pip install scipy
pip install dlib
pip install face_recognition
pip install flask

@author: ramin

"/home/ramin/git/datascience/faceVerification/images/flask/"

"""
import face_recognition
from PIL import Image, ImageDraw
from flask import Flask
from flask import request
from datetime import datetime


import json

print(json.dumps(["apple", "bananas"]))

print("------------------------------------------------------------------")
print(">>>>>>>>>>>>>>>>>>>>>>> State1        " + str(datetime.utcnow().strftime('%d.%m.%Y %H:%M:%S.%f')[:-3]))





fileStore = '/home/ramin/git/datascience/faceVerification/images/face/menar/'
targetFile = '0.jpg'
sourceFile = 'family.jpg'
resultFile = 'rrrr.jpg'

print("fileStore="+str(fileStore))

## Image Path
img1 = fileStore+targetFile
img2 = fileStore+sourceFile


known_image = face_recognition.load_image_file(img1)
unknown_image = face_recognition.load_image_file(img2)

print(">>>>>>>>>>>>>>>>>>>>>>> State2        " + str(datetime.utcnow().strftime('%d.%m.%Y %H:%M:%S.%f')[:-3]))
#pil_im = Image.open(img1)
#display(pil_im)


result = "";
####### Detect Face Location in known object
known_face_locations = None
for i in range(1, 4):
    known_face_locations = face_recognition.face_locations(known_image, number_of_times_to_upsample=i)
    if not known_face_locations:
        print(" try to find face in target object failed  - deep: " + str(i))
    else:
        break

if not known_face_locations:
    result = "no face detected in target image"
    #TO DO - RETURN
known_encoding = face_recognition.api.face_encodings(known_image, known_face_locations=known_face_locations)[0]
print(">>>>>>>>>>>>>>>>>>>>>>> State3        " + str(datetime.utcnow().strftime('%d.%m.%Y %H:%M:%S.%f')[:-3]))    





unKnown_face_locations = face_recognition.face_locations(unknown_image, number_of_times_to_upsample=0)


####### Detect Face Location in unKnown object
for i in range(4, 4):
    unKnown_face_locations = face_recognition.face_locations(unknown_image, number_of_times_to_upsample=i)
    if not unKnown_face_locations:
        print(" try to find face in source object failed  - deep: " + str(i))
    else:
        break

unknown_encoding = face_recognition.api.face_encodings(unknown_image, known_face_locations=unKnown_face_locations)
print(">>>>>>>>>>>>>>>>>>>>>>> State4        " + str(datetime.utcnow().strftime('%d.%m.%Y %H:%M:%S.%f')[:-3]))

## Constants
known_face_encodings = [ known_encoding ]


# Find all the faces and face encodings in the unknown image
face_locations = unKnown_face_locations
face_encodings = unknown_encoding

# Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
# See http://pillow.readthedocs.io/ for more about PIL/Pillow
pil_image = Image.fromarray(unknown_image)
# Create a Pillow ImageDraw Draw instance to draw with
draw = ImageDraw.Draw(pil_image)

# Loop through each face found in the unknown image
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    # See if the face is a match for the known face(s)
    #matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    print(">>>>>>>>>>>>>>>>>>>>>>> State5        " + str(datetime.utcnow().strftime('%d.%m.%Y %H:%M:%S.%f')[:-3]))
    name = ""
    
    # Or instead, use the known face with the smallest distance to the new face
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    print(face_distances)
    
    same_person = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance = 0.5)
    print("same_person = " + str(same_person))
    
    if (same_person[0] == True):
        result = "Target face detected in source image, tolerance = " + str(face_distances)
        name = "Target"
    else:
        name = "Unknown"
    
    #best_match_index = np.argmin(face_distances)
    #if matches[best_match_index]:
    #    name = known_face_names[best_match_index]
        
    # Draw a box around the face using the Pillow module
    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

    # Draw a label with a name below the face
    text_width, text_height = draw.textsize(name)
    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
    draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))


print(">>>>>>>>>>>>>>>>>>>>>>> State6        " + str(datetime.utcnow().strftime('%d.%m.%Y %H:%M:%S.%f')[:-3]))

if (result == ""):
    result = "target face NOT detected in source image"

# Remove the drawing library from memory as per the Pillow docs
del draw

print(">>>>>>>>>>>>>>>>>>>>>>> State7        " + str(datetime.utcnow().strftime('%d.%m.%Y %H:%M:%S.%f')[:-3]))
# Save image
pil_image.save(fileStore+resultFile)
print("image saved")
    

