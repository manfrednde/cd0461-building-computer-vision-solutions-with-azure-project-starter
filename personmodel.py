import sys
import os

sys.path.append("/Users/manfrednde/Library/Python/3.9/lib/python/site-packages")

import io
import datetime
import pandas as pd
from PIL import Image
import requests
import io
import glob, os, sys, time, uuid

from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt


from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw

from video_indexer import VideoIndexer
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import TrainingStatusType
from msrest.authentication import CognitiveServicesCredentials

CONFIG = {
    'SUBSCRIPTION_KEY': '621d1daaa9ff4041bc484d4f7b9d5d10',
    'LOCATION': 'trial',
    'ACCOUNT_ID': '6723d089-da1a-41ab-ae6a-7074c23d084b'
}

video_analysis = VideoIndexer(
    vi_subscription_key=CONFIG['SUBSCRIPTION_KEY'],
    vi_location=CONFIG['LOCATION'],
    vi_account_id=CONFIG['ACCOUNT_ID']
)

video_analysis.check_access_token()

video_id = '30fa204ae0'

video_analysis.get_video_info(video_id)

info = video_analysis.get_video_info(video_id, video_language='English')

if len(info['videos'][0]['insights']['faces'][0]['thumbnails']):
    print("We found {} faces in this video.".format(str(len(info['videos'][0]['insights']['faces'][0]['thumbnails']))))

info['videos'][0]['insights']['faces'][0]['thumbnails']

images = []
img_raw = []
img_strs = []
for each_thumb in info['videos'][0]['insights']['faces'][0]['thumbnails']:
    if 'fileName' in each_thumb and 'id' in each_thumb:
        file_name = each_thumb['fileName']
        thumb_id = each_thumb['id']
        img_code = video_analysis.get_thumbnail_from_video_indexer(video_id,  thumb_id)
        img_strs.append(img_code)
        img_stream = io.BytesIO(img_code)
        img_raw.append(img_stream)
        img = Image.open(img_stream)
        images.append(img)

for img in images:
    print(img.info)
    plt.figure()
    plt.imshow(img)

i = 1
for img in images:
    print(type(img))
    img.save('human-face' + str(i) + '.jpg')
    i= i+ 1


thumbnail_id = "40294a85-eb72-4085-84c4-081e094ac866"

img_code = video_analysis.get_thumbnail_from_video_indexer(video_id,  thumbnail_id)
print(img_code)


img_code = video_analysis.get_thumbnail_from_video_indexer(video_id,  thumbnail_id)
img_stream = io.BytesIO(img_code)
img = Image.open(img_stream)
imshow(img)


keyframes = []
for shot in info["videos"][0]["insights"]["shots"]:
    for keyframe in shot["keyFrames"]:
        keyframes.append(keyframe["instances"][0]['thumbnailId'])


for keyframe in keyframes:
    img_str = video_analysis.get_thumbnail_from_video_indexer(video_id,  keyframe)

print('sentiments')
print(info['summarizedInsights']['sentiments'])
info['summarizedInsights']['sentiments']

info['summarizedInsights']['emotions']


FACE_KEY = "72c95a765bb54e47a54fb8f33f290252"
FACE_ENDPOINT = "https://face-boarding.cognitiveservices.azure.com"

face_client = FaceClient(FACE_ENDPOINT, CognitiveServicesCredentials(FACE_KEY))

face_client.api_version

print("API VERSION")
print(face_client.api_version)

PERSON_GROUP_ID = str(uuid.uuid4())
person_group_name = 'person-manfred'

def build_person_group(client, person_group_id, pgp_name):
    print('Create and build a person group...')
    # Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
    print('Person group ID:', person_group_id)
    # client.person_group.create(person_group_id = person_group_id, name=person_group_id)
    client.person_group.create(person_group_id = person_group_id, name=pgp_name)

    # Create a person group person.
    human_person = client.person_group_person.create(person_group_id, pgp_name)
    # Find all jpeg human images in working directory.
    human_face_images = [file for file in glob.glob('*.jpg') if file.startswith("human-face")]
    # Add images to a Person object
    for image_p in human_face_images:
        with open(image_p, 'rb') as w:
            client.person_group_person.add_face_from_stream(person_group_id, human_person.person_id, w)

    # Train the person group, after a Person object with many images were added to it.
    client.person_group.train(person_group_id)

    # Wait for training to finish.
    while (True):
        training_status = client.person_group.get_training_status(person_group_id)
        print("Training status: {}.".format(training_status.status))
        if (training_status.status is TrainingStatusType.succeeded):
            break
        elif (training_status.status is TrainingStatusType.failed):
            client.person_group.delete(person_group_id=PERSON_GROUP_ID)
            sys.exit('Training the person group has failed.')
        time.sleep(5)


build_person_group(face_client, PERSON_GROUP_ID, person_group_name)

'''
Detect all faces in query image list, then add their face IDs to a new list.
'''
# def detect_faces(client, query_images_list):
#     print('Detecting faces in query images list...')

#     face_ids = {} # Keep track of the image ID and the related image in a dictionary
#     for image_name in query_images_list:
#         image = open(image_name, 'rb') # BufferedReader
#         print("Opening image: ", image.name)
#         time.sleep(5)

#         # Detect the faces in the query images list one at a time, returns list[DetectedFace]
#         faces = client.face.detect_with_stream(image)  

#         # Add all detected face IDs to a list
#         for face in faces:
#             print('Face ID', face.face_id, 'found in image', os.path.splitext(image.name)[0]+'.jpg')
#             # Add the ID to a dictionary with image name as a key.
#             # This assumes there is only one face per image (since you can't have duplicate keys)
#             face_ids[image.name] = face.face_id

#     return face_ids


# test_images = [file for file in glob.glob('*.jpg') if file.startswith("human-face")]

# test_images

# ids = detect_faces(face_client, test_images)

# ids