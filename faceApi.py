import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw

# https://learn.udacity.com/nanodegrees/nd073/parts/cd0461/lessons/497841e6-1dcf-403d-b1e2-c6567e69b702/concepts/8e6aa492-1e4f-4eff-9ff5-20abc652c4d9

# https://learn.udacity.com/nanodegrees/nd073/parts/cd0461/lessons/497841e6-1dcf-403d-b1e2-c6567e69b702/concepts/e0357691-4320-4c14-9e50-2ef4017caeec# 

https://learn.udacity.com/nanodegrees/nd073/parts/cd0461/lessons/497841e6-1dcf-403d-b1e2-c6567e69b702/concepts/800d3f9f-b4d8-472b-b541-3bc28a4ee729

sys.path.append("/Users/manfrednde/Library/Python/3.9/lib/python/site-packages")

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person


import matplotlib.pyplot as plt

def show_image_in_cell(face_url):
    response = requests.get(face_url)
    img = Image.open(BytesIO(response.content))
    plt.figure(figsize=(20,10))
    plt.imshow(img)
    plt.show()

def show_image_object_in_cell(image_object):
    plt.figure(figsize=(20,10))
    plt.imshow(image_object)
    plt.show()

def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    
    return ((left, top), (right, bottom))

def drawFaceRectangles(source_file, detected_face_object) :
    # Download the image from the url
    response = requests.get(source_file)
    img = Image.open(BytesIO(response.content))
    # Draw a red box around every detected faces
    draw = ImageDraw.Draw(img)
    for face in detected_face_object:
        draw.rectangle(getRectangle(face), outline='red', width= 10)
    return img

KEY = "2f1dc845985743c6b7658a77d646dc3c"
ENDPOINT = "https://face-api-boarding-kiosk.cognitiveservices.azure.com/"

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
face_client.api_version

group_face_01 = "https://raw.githubusercontent.com/udacity/cd0461-building-computer-vision-solutions-with-azure-exercises/main/resources/group-faces-01.jpg"
group_face_02 = "https://raw.githubusercontent.com/udacity/cd0461-building-computer-vision-solutions-with-azure-exercises/main/resources/group-faces-02.jpg"
group_face_03 = "https://raw.githubusercontent.com/udacity/cd0461-building-computer-vision-solutions-with-azure-exercises/main/resources/group-faces-03.jpg"
group_face_04 = "https://raw.githubusercontent.com/udacity/cd0461-building-computer-vision-solutions-with-azure-exercises/main/resources/group-faces-04.jpg"


single_face_x = "https://raw.githubusercontent.com/udacity/cd0461-building-computer-vision-solutions-with-azure-exercises/main/resources/obama-photo.jpg"
single_face = "https://raw.githubusercontent.com/udacity/cd0461-building-computer-vision-solutions-with-azure-exercises/main/resources/face-portrait.jpg"

show_image_in_cell(single_face_x)

show_image_in_cell(single_face)

selected_image = single_face


# Detect Face form an image
def detect_face_from_any_url(selected_image):
    detected_faces = face_client.face.detect_with_url(url=selected_image, detection_model='detection_03')
    if not detected_faces:
        raise Exception('No face detected from image {}'.format(single_image_name))        
    print('Total face(s) detected  from {}'.format(str(len(detected_faces))))
    return detected_faces

def list_all_faces_from_detected_face_object(detected_faces_object):
    print('We found total {} face(s) in selected face detected object.'.format(str(len(detected_faces_object))))
    for face in detected_faces_object: 
        print (face.face_id)

detected_faces_object = detect_face_from_any_url(selected_image)

list_all_faces_from_detected_face_object(detected_faces_object)

drawFaceRectangles(selected_image, detected_faces_object)

selected_image_2 = single_face_x

detected_faces_object = detect_face_from_any_url(selected_image_2)

list_all_faces_from_detected_face_object(detected_faces_object)

drawFaceRectangles(selected_image_2, detected_faces_object)

# Face detection in group
selected_image_3 = group_face_01
detected_faces_object_3 = detect_face_from_any_url(selected_image_3)
list_all_faces_from_detected_face_object(detected_faces_object_3)
drawFaceRectangles(selected_image_3, detected_faces_object_3)

show_image_in_cell(selected_image_3)