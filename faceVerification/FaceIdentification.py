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
import face_recognition
from PIL import Image, ImageDraw
from flask import Flask

app = Flask(__name__)


@app.route("/faceiden")
def faceIden(targetFile, sourceFile):
    #import numpy as np    
    #import face_recognition
    #from PIL import Image, ImageDraw
    #from IPython.display import display
    
    
    ## Image Path
    img1 = "/home/ramin/git/datascience/faceVerification/images/flask/"+targetFile
    img2 = "/home/ramin/git/datascience/faceVerification/images/flask/"+sourceFile
    deepLevel = 3
    
    
    known_image = face_recognition.load_image_file(img1)
    unknown_image = face_recognition.load_image_file(img2)
    
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
        return result
        #TO DO - RETURN
    known_encoding = face_recognition.api.face_encodings(known_image, known_face_locations=known_face_locations)[0]
    
    
    ####### Detect Face Location in unKnown object
    unKnown_face_locations = face_recognition.face_locations(unknown_image, number_of_times_to_upsample=deepLevel)
    if not unKnown_face_locations:
        result = "no face detected in source image"
        return result
        #TO DO - RETURN
    
    unknown_encoding = face_recognition.api.face_encodings(unknown_image, known_face_locations=unKnown_face_locations)
    
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
    
        name = ""
        
        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        print(face_distances)
        
        if (100-face_distances*100 > 60):
            result = "target face detected in source image"
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
    
    
    if (result == ""):
        result = "target face NOT detected in source image"
    
    # Remove the drawing library from memory as per the Pillow docs
    del draw
    
   
    # Save image
    pil_image.save("/home/ramin/git/datascience/faceVerification/images/flask/source.jpg")
    print("image saved")
    
    return result


## RUN APPLICATION
if __name__ == '__main__':
    app.run(debug=True)