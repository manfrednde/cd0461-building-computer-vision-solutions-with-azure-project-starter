import sys
import os

sys.path.append("/Users/manfrednde/Library/Python/3.9/lib/python/site-packages")

# Importing Useful Python Libraries or Packages
import asyncio
import io
import glob
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw


from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person


import matplotlib.pyplot as plt


from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw

from video_indexer import VideoIndexer
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import TrainingStatusType
from msrest.authentication import CognitiveServicesCredentials

CONFIG = {
    'SUBSCRIPTION_KEY': '6c39f60b-2bb1-4e37-ad64-faaf30beaca4',
    'LOCATION': 'trial',
    'ACCOUNT_ID': '6723d089-da1a-41ab-ae6a-7074c23d084b'
}

video_analysis = VideoIndexer(
    vi_subscription_key=CONFIG['SUBSCRIPTION_KEY'],
    vi_location=CONFIG['LOCATION'],
    vi_account_id=CONFIG['ACCOUNT_ID']
)

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

# TAKEN FROM THE Azure SDK Sample
# Convert width height to a point in a rectangle
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
        draw.rectangle(getRectangle(face), outline='red', width = 10)
    return img

FACE_KEY = "edbe59bfc1a14ae09e80d4c7934f384b"
FACE_ENDPOINT = "https://face-boarding.cognitiveservices.azure.com"

face_client = FaceClient(FACE_ENDPOINT, CognitiveServicesCredentials(FACE_KEY))

face_client.api_version
face_image = "https://raw.githubusercontent.com/manfrednde/cd0461-building-computer-vision-solutions-with-azure-project-starter/master/starter/digital_id_template/ca-dl-libby-herold.png"
selected_image = face_image

# show_image_in_cell(face_image)

# Detect Face form an image
def detect_face_from_any_url(selected_image):
    detected_faces = face_client.face.detect_with_url(url=selected_image, detection_model='detection_03')
    if not detected_faces:
        raise Exception('No face detected from image {}'.format(selected_image))     
    print('Total face(s) detected  from {}'.format(str(len(detected_faces)))) # type: ignore
    return detected_faces

# Define a function to output the faces detected
def list_all_faces_from_detected_face_object(detected_faces_object):
    print('We found total {} face(s) in selected face detected object.'.format(str(len(detected_faces_object))))
    face_ids =  []
    for face in detected_faces_object: 
        face_ids.append(face.face_id)
        print (face.face_id)
        print (face)
    return face_ids

detected_faces_object = detect_face_from_any_url(selected_image)

face_ids_from_id_card = list_all_faces_from_detected_face_object(detected_faces_object)



# similar_faces = face_client.face.find_similar(face_id=source_image_face_id, face_ids=group_image_face_IDs_list)

# for similar_face in similar_faces:
#     print(similar_face.face_id)


# verify_result_same = face_client.face.verify_face_to_face(source_image_face_id, face_ids_from_id_card[0])

# print('Faces from {} & {} are of the same person, with confidence: {}'.format(source_image, selected_image_2, verify_result_same.confidence))
# if verify_result_same.is_identical:
#     print("Faces are Similar")
# else:
#     print('Faces from {} & {} are of a different person, with confidence: {}'.format(source_image, selected_image_2, verify_result_same.confidence))