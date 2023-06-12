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

uploaded_video_id = video_analysis.upload_to_video_indexer(
   input_filename='/Users/manfrednde/Desktop/PROJECT-1-FINAL/Step0/Video/avkash-boarding-pass.mp4',
   video_name='manfred-test-video',  # unique identifier for video in Video Indexer platform
   video_language='English'
)

uploaded_video_id

info = video_analysis.get_video_info(uploaded_video_id, video_language='English')

info