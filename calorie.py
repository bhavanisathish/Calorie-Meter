import cv2
import numpy as np
import RPi.GPIO as GPIO          #Import GPIO library
import time
import datetime
import json
from watson_developer_cloud import VisualRecognitionV3
#Import time library
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
import json
from ibm_watson import TextToSpeechV1 #pip install --upgrade "ibm-watson>=3.2.0"
from ibm_watson.websocket import SynthesizeCallback
#To install the pydub command is pip install pydub
from pydub import AudioSegment
from pydub.playback import play
import tkFileDialog as filedialog
from Tkinter import *
#root=Tk()

def speechreg(k,p):
    if(p=='biryani' or p=='jambalaya'):
        global z
        s='           the calorie content of biriyani/jambalaya is 400 to 600 '
        o='the food is'+p
        z=o+s
    elif(p=='rice'):
        global z
        s='           the calorie content of fried rice is 130'
        o='the food is fried'+p
        z=o+s
    elif(p=='roast chicken'):
        global z
        s='           the calorie content of roast chicken is 240'
        o='the food is fried'+p
        z=o+s
    elif(p=='boiled egg'):
        global z
        s='           the calorie content of boiled egg is 155'
        o='the food is fried'+p
        z=o+s
    
    service = TextToSpeechV1(
    ## url is optional, and defaults to the URL below. Use the correct URL for your region.
    
       
    url='https://gateway-lon.watsonplatform.net/text-to-speech/api',
    iam_apikey='AlBMRdLEg-qoOA5lzpmP48Uhf-OM-5BuHTMkHVO935dM')
    with open("/home/pi/Documents/harish.wav", 'wb') as audio_file:
        audio_file.write(
            service.synthesize(
            z,
            voice='en-US_AllisonVoice',
            accept='audio/wav'        
        ).get_result().content)
    
    song = AudioSegment.from_wav("/home/pi/Documents/harish.wav")
    play(song)
     


def imagerecognise(k):
   visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='GrJevtixcMt7wZ8v3Yxy7UOnUN_TMmHUAWGboiYAzGUC')
   with open(k, 'rb') as images_file:
        classes = visual_recognition.classify(
        images_file,
        threshold='0.6',
	classifier_ids='food'
        ).get_result()
   print(json.dumps(classes, indent=2))
   p=classes['images'][0]['classifiers'][0]['classes'][0]['class']
   print(p)
   
   speechreg(k,p)
    


GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Enable input and pull up resistors
while True:
    input_state = GPIO.input(12) #Read and store value of input to a variable
    if (input_state == 0):     #Check whether pin is grounded
       print('on')
       print('press the key to know the calorie of the trained food')
       print('1-biriyani')
       #k='fried.png'
       #cap=cv2.VideoCapture(0)
       while True:
            #ret,frame=cap.read()
            #s=datetime.datetime.now()
            
            s=filedialog.askopenfilename()
            k=s #'2019-09-14 10:54:43.564874.png'#str(s)+'.png'
            print('hi')
            #cv2.imwrite(k,frame)
            #cv2.imshow('food',frame)
            print('hi')
            time.sleep(2)
            imagerecognise(k)
            break
               
    else:
        print('off')
        
    time.sleep(5)
