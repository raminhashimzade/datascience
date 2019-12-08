#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 22:39:11 2019

@author: ramin
"""



import speech_recognition as sr

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    
r = sr.Recognizer()

while True :
    with sr.Microphone() as source:
        audio = r.listen(source,timeout=1,phrase_time_limit=3)
        
    try:
        print(r.recognize_google(audio))
    except:
        pass;
    
