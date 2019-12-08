# -*- coding: utf-8 -*-

import pyttsx3 
  
# initialisation 
engine = pyttsx3.init() 
 
# testing 
#engine.setProperty('voice', "english")

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) 

engine.say("Nurlan Rəşaddan yaxşı oğlandı. Amma Ceyhunda pis deyil") 

engine.say("Rəşaddan potabaşdı") 
engine.say("Azad armuddu") 
engine.say("Nulan porsuzxdu") 

engine.runAndWait()



for voice in voices:
    print("Voice:")
    print(" - ID: %s" % voice.id)
    print(" - Name: %s" % voice.name)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)
    

def onStart(): 
   print('starting') 
  
def onWord(name, location, length): 
   print('word', name, location, length) 
  
def onEnd(name, completed): 
   print('finishing', name, completed) 
  
engine = pyttsx3.init() 
  
engine.connect('started-utterance', onStart) 
engine.connect('started-word', onWord) 
engine.connect('finished-utterance', onEnd) 
  
sen = 'Geeks for geeks is a computer portal for Geeks'
  
  
engine.say(sen) 
engine.runAndWait() 




import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    print(voice, voice.id)
    engine.setProperty('voice', voice.id)
    engine.say("Nurlan Rəşaddan yaxşı oğlandı. Amma Ceyhunda pis deyil")
    engine.runAndWait()
    engine.stop()