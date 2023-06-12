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
%matplotlib inline

from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw

from video_indexer import VideoIndexer
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import TrainingStatusType
from msrest.authentication import CognitiveServicesCredentials

CONFIG = {
    'SUBSCRIPTION_KEY': 'YOUR VIDEO INDEXER SUBSCRIPTION KEY',
    'LOCATION': 'trial',
    'ACCOUNT_ID': 'YOUR VIDEO INDEXER ACCOUNT ID'
}

video_analysis = VideoIndexer(
    vi_subscription_key=CONFIG['SUBSCRIPTION_KEY'],
    vi_location=CONFIG['LOCATION'],
    vi_account_id=CONFIG['ACCOUNT_ID']
)

video_analysis.check_access_token()

video_id = 'ENTER YOUR VIDEO ID'

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

!ls human-face*.jpg

# Enter one of the thumbnail output you got from the previous cell, 
# under the "Getting Thumbnail ID from the Analysis JSON" section.
thumbnail_id='ENTER THUMBNAIL HERE'

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


info['summarizedInsights']['sentiments']
info['summarizedInsights']['emotions']