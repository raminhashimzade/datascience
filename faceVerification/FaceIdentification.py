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
import json
import logging


app = Flask(__name__)
logging.basicConfig(filename='./logs/model.log', format='%(asctime)s:::%(levelname)s:::%(message)s', level=logging.INFO)

@app.route("/faceiden", methods=['POST'])
def faceIden():
    face, tolerance = [], []
    
    
    logging.info("------------------------------------------------------------------")
    logging.info(">>>>>>>>>>>>>>>>>>>>>>> State1")    
    logging.info("request="+str(request.get_json()))
    
    req_data = request.get_json(force=True)
    fileStore = req_data['fileStore']    
    targetFile = req_data['targetFile']
    sourceFile = req_data['sourceFile']
    resultFile = req_data['resultFile']
    
    
    logging.info("fileStore="+str(fileStore))
    
    ## Image Path
    img1 = fileStore+targetFile
    img2 = fileStore+sourceFile
    
    
    known_image = face_recognition.load_image_file(img1)
    unknown_image = face_recognition.load_image_file(img2)
    
    
    logging.info(">>>>>>>>>>>>>>>>>>>>>>> State2")
    #pil_im = Image.open(img1)
    #display(pil_im)
    
    
    result = "";
    ####### Detect Face Location in known object
    known_face_locations = None
    #for i in range(0, 4):
    for i in reversed(range(4)):
        known_face_locations = face_recognition.face_locations(known_image, number_of_times_to_upsample=i)
        if not known_face_locations:
            logging.info(" try to find face in target object failed  - deep: " + str(i))
        else:
            break
    
    if not known_face_locations:
        result = "no face detected in target image"
        return result
        #TO DO - RETURN
    known_encoding = face_recognition.api.face_encodings(known_image, known_face_locations=known_face_locations)[0]
    logging.info(">>>>>>>>>>>>>>>>>>>>>>> State3")
    
    ####### Detect Face Location in unKnown object
    #for i in range(0, 4):
    for i in reversed(range(4)):
        unKnown_face_locations = face_recognition.face_locations(unknown_image, number_of_times_to_upsample=i)
        if not unKnown_face_locations:
            logging.info(" try to find face in source object failed  - deep: " + str(i))
        else:
            break
    
    unknown_encoding = face_recognition.api.face_encodings(unknown_image, known_face_locations=unKnown_face_locations)
    logging.info(">>>>>>>>>>>>>>>>>>>>>>> State4")
    
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
    
    target = []
    samePerson = []
    n = 1
    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        #matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        logging.info(">>>>>>>>>>>>>>>>>>>>>>> State5")
        name = ""
        
        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        logging.info(face_distances)
        
        same_person = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance = 0.55)
        logging.info("same_person = " + str(same_person))
        
        if (same_person[0] == True):
            name = "Target-"+str(n)
            target.append(name)
            samePerson.append(True)
        else:
            name = "Unknown-"+str(n)
            samePerson.append(False)
            
        face.append(name)
        tolerance.append(face_distances[0])
        
        #best_match_index = np.argmin(face_distances)
        #if matches[best_match_index]:
        #    name = known_face_names[best_match_index]
            
        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
    
        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
        n += 1
    
    
    logging.info(">>>>>>>>>>>>>>>>>>>>>>> State6")
    
    
    if (target == []):
        result = "Target face NOT detected in source image"
    else:
        result = "Target face detected in source image : " + ','.join(target)
    
    # Remove the drawing library from memory as per the Pillow docs
    del draw
    
    # Save image
    pil_image.save(fileStore+resultFile)
    logging.info("image saved")
    
    score_titles = [{"face": t, "tolerance": s, "samePerson": b} for t, s, b in zip(face, tolerance, samePerson)]
    
    result = '{"resultText" :"'+result+'","faces":'+json.dumps(score_titles)+' }'
    
    logging.info("result : " + result)
    return result


## RUN APPLICATION
if __name__ == '__main__':
    app.run(debug=True)
