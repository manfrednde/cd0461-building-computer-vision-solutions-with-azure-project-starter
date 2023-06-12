import sys
import os
import datetime

from PIL import Image
import io

from matplotlib.pyplot import imshow
import matplotlib.pyplot as plt


from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
import requests
from io import BytesIO

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

sys.path.append("/Users/manfrednde/Library/Python/3.9/lib/python/site-packages")

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import FormTrainingClient
from azure.core.credentials import AzureKeyCredential

import pandas as pd

AZURE_FORM_RECOGNIZER_ENDPOINT = "https://formrecogniserbaording.cognitiveservices.azure.com/"
AZURE_FORM_RECOGNIZER_KEY = "ad34b28b260a428f8c19e2dd366d0568"

endpoint = AZURE_FORM_RECOGNIZER_ENDPOINT
key = AZURE_FORM_RECOGNIZER_KEY

FACEIMAGE = "https://raw.githubusercontent.com/manfrednde/cd0461-building-computer-vision-solutions-with-azure-project-starter/master/starter/digital_id_template/ca-dl-avkash-chauhan.png"

NEWTESTURL = "https://stbaordingkiosk.blob.core.windows.net/kiosk-container/boarding-avkash.pdf?sp=rcwd&st=2023-05-30T02:02:41Z&se=2023-07-08T10:02:41Z&sv=2022-11-02&sr=b&sig=WJVy6ScPlpk7%2FnCScaYBYJ5S%2BT80IWw3RTUWz08WXEA%3D"

form_recognizer_client = FormRecognizerClient(endpoint=endpoint, credential=AzureKeyCredential(key))

path_to_sample_documents = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "..",
            "./starter/digital_id_template/ca-dl-avkash.png",
        )
    )

with open(path_to_sample_documents, "rb") as f: 
    id_content_from_url = form_recognizer_client.begin_recognize_identity_documents(identity_document=f)

collected_id_cards = id_content_from_url.result()

collected_id_cards

type(collected_id_cards[0])

# Processing the results
def get_id_card_details(identity_card):

    first_name = identity_card.fields.get("FirstName")
    if first_name:
        print("First Name: {} has confidence: {}".format(first_name.value, first_name.confidence))
    last_name = identity_card.fields.get("LastName")
    if last_name:
        print("Last Name: {} has confidence: {}".format(last_name.value, last_name.confidence))
    document_number = identity_card.fields.get("DocumentNumber")
    if document_number:
        print("Document Number: {} has confidence: {}".format(document_number.value, document_number.confidence))
    dob = identity_card.fields.get("DateOfBirth")
    if dob:
        print("Date of Birth: {} has confidence: {}".format(dob.value, dob.confidence))
    doe = identity_card.fields.get("DateOfExpiration")
    if doe:
        print("Date of Expiration: {} has confidence: {}".format(doe.value, doe.confidence))
    sex = identity_card.fields.get("Sex")
    if sex:
        print("Sex: {} has confidence: {}".format(sex.value, sex.confidence))
    address = identity_card.fields.get("Address")
    if address:
        print("Address: {} has confidence: {}".format(address.value, address.confidence))
    country_region = identity_card.fields.get("CountryRegion")
    if country_region:
        print("Country/Region: {} has confidence: {}".format(country_region.value, country_region.confidence))
    region = identity_card.fields.get("Region")
    if region:
        print("Region: {} has confidence: {}".format(region.value, region.confidence))

    return first_name.value, last_name.value, dob.value

idFirstName, idLastName, idDob = get_id_card_details(collected_id_cards[0])

print(idFirstName)
print(idLastName)
print(idDob)


############### DONE ready from ID

form_training_client = FormTrainingClient(endpoint=endpoint, credential=AzureKeyCredential(key))

saved_model_list = form_training_client.list_custom_models()

custom_model_info = form_training_client.get_custom_model(model_id="1a8a813a-339c-475b-a438-307bab368d3a")
# custom_model_info = form_training_client.get_custom_model(model_id=custom_model.model_id)
print("Model ID: {}".format(custom_model_info.model_id))
print("Status: {}".format(custom_model_info.status))
print("Training started on: {}".format(custom_model_info.training_started_on))
print("Training completed on: {}".format(custom_model_info.training_completed_on))


# Using an image document as test document URL (Not using PDF here)

new_test_url = NEWTESTURL

form_recognizer_client = FormRecognizerClient(endpoint=endpoint, credential=AzureKeyCredential(key))

custom_model_info.model_id

custom_test_action = form_recognizer_client.begin_recognize_custom_forms_from_url(model_id=custom_model_info.model_id, form_url=new_test_url)

custom_test_action.status()

custom_test_action_result = custom_test_action.result()


boardingPassPassengerName = ""
boardingPassFlightNumber = ""
boardingPassSeat = 0
boardingPassClass = ""
boardingPassOrigin = ""
boardingPassDestination = ""
boardingPassFlightDate = "April 20, 2022"
boardingPassFlightTime = "10:00 AM PST"

for recognized_content in custom_test_action_result:
    print("Form type: {}".format(recognized_content.form_type))
    for name, field in recognized_content.fields.items():
        print("Field '{}' has label '{}' with value '{}' and a confidence score of {}".format(
            name,
            field.label_data.text if field.label_data else name,
            field.value,
            field.confidence
        ))
        if name == 'Passenger Name':
            boardingPassPassengerName = str(field.value).lower()
            print(boardingPassPassengerName)
        if name == 'Flight Number':
            boardingPassFlightNumber = str(field.value).lower()
            print(boardingPassFlightNumber)
        if name == 'Seat':
            boardingPassSeat = field.value
            print(boardingPassSeat)
        if name == 'Class':
            boardingPassClass = field.value
            print(boardingPassClass)
        if name == 'From':
            boardingPassOrigin = str(field.value).lower()
            print(boardingPassOrigin)
        if name == 'To':
            boardingPassDestination = str(field.value).lower()
            print(boardingPassDestination)
        if name == 'Date':
            boardingPassFlightDate = field.value
            print(boardingPassFlightDate)
        if name == 'Boarding Time':
            boardingPassFlightTime = field.value
            print(boardingPassFlightTime)

# reading the csv file
df = pd.read_csv("./starter/step0/FlightManifest.csv")
CUSTOMER_INDEX = 0
DateofBirth = False
NameValidation = False
DoBValidation = False
PersonValidation = False
BoardingPassValidation = False
LuggageValidation = False
PassengerFullName = ""

for index, row in df.iterrows():
    manifestPassengerFullName = row['First Name'].lower() + " " + row['Last Name'].lower()
    manifestDateofBirth = datetime.datetime.strptime(row['DateofBirth'], '%d %B %Y').date()
    print(manifestPassengerFullName)
    print(manifestDateofBirth)

    if row['First Name'].lower() == idFirstName.lower() and row['Last Name'].lower() == idLastName.lower() and boardingPassPassengerName == manifestPassengerFullName:
        df.at[index, 'NameValidation'] = True
        print(index)
        CUSTOMER_INDEX = index
        NameValidation = True
        PassengerFullName = manifestPassengerFullName
        print(row['First Name'])
        print(row['Last Name'])
        # writing into the file
        df.to_csv("./starter/step0/FlightManifest.csv", index=False)

    if manifestDateofBirth == idDob:
        df.at[index, 'DoBValidation'] = True
        print(index)
        print(row['DateofBirth'])
        DoBValidation = True
        # writing into the file
        df.to_csv("./starter/step0/FlightManifest.csv", index=False)

    if row['Flight No.'] == boardingPassFlightNumber and row['seat'] == boardingPassSeat and row['Class'] == boardingPassClass and row['From'] == boardingPassOrigin and row['To'] == boardingPassDestination and row['Boarding Time'] == boardingPassFlightTime and row['Date'] == boardingPassFlightDate:
        df.at[index, 'BoardingPassValidation'] = True
        print("Boarding Pass Validated")
        print(index)
        BoardingPassValidation = True
        df.to_csv("./starter/step0/FlightManifest.csv", index=False)


###########################

# Detect face



video_analysis.check_access_token()

video_id = '30fa204ae0'

video_analysis.get_video_info(video_id)

info = video_analysis.get_video_info(video_id, video_language='English')

if len(info['videos'][0]['insights']['faces'][0]['thumbnails']):
    print("We found {} faces in this video.".format(str(len(info['videos'][0]['insights']['faces'][0]['thumbnails']))))

# info['videos'][0]['insights']['faces'][0]['thumbnails']

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
    # print(type(img))
    img.save('human-face' + str(i) + '.jpg')
    i= i+ 1


######

# FACE 

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

# # Convert width height to a point in a rectangle
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

FACE_KEY = "7fdd7dabd63240ff9a8f0f29f2fc4411"
FACE_ENDPOINT = "https://face-boarding1.cognitiveservices.azure.com"

face_client = FaceClient(FACE_ENDPOINT, CognitiveServicesCredentials(FACE_KEY))

face_client.api_version
face_image = FACEIMAGE
selected_image = face_image


# Detect Face form an image
def detect_face_from_any_url(selected_image):
    detected_faces = face_client.face.detect_with_url(url=selected_image, detection_model='detection_03')
    if not detected_faces:
    	  raise Exception('No face detected from image {}'.format(single_image_name))        
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



def detect_face_from_stream(selected_image):
    detected_faces = face_client.face.detect_with_stream(selected_image, detection_model='detection_03')
    if not detected_faces:
         raise Exception('No face detected from image {}'.format(single_image_name))        
    print('Total face(s) detected  from {}'.format(str(len(detected_faces)))) # type: ignore
    return detected_faces


face_fd =  open("human-face1.jpg", "rb")

video_detected_faces_object = detect_face_from_stream(face_fd)

face_ids_from_video = list_all_faces_from_detected_face_object(video_detected_faces_object)


verify_result_same = face_client.face.verify_face_to_face(face_ids_from_video[0], face_ids_from_id_card[0])

if verify_result_same.is_identical: # type: ignore
    print("Faces are Similar")
    print('Faces from {} & {} are of the same person, with confidence: {}'.format(face_ids_from_video[0], face_ids_from_id_card[0], verify_result_same.confidence)) # type: ignore
    df.at[CUSTOMER_INDEX, 'PersonValidation'] = True
    PersonValidation = True
    # writing into the file
    df.to_csv("./starter/step0/FlightManifest.csv", index=False)
else:
    print("Faces are not Similar")
    print('Faces from {} & {} are of a different person, with confidence: {}'.format(face_ids_from_video[0], face_ids_from_video[0], verify_result_same.confidence)) # type: ignore
    df.at[CUSTOMER_INDEX, 'PersonValidation'] = False
    # writing into the file
    df.to_csv("./starter/step0/FlightManifest.csv", index=False)
face_fd.close()


if (NameValidation == False) or (DoBValidation == False):

    cmd = """Dear {},\n
      You are welcome to flight # {} leaving at {} from {} to {}.\n
      Your seat number is {}, and it is confirmed.\n
      We did not find a prohibited item (lighter) in your carry-on baggage.\n
      Thanks for following the procedure.\n
      Your identity could not be verified. Please see a customer service representative.""".format(
      boardingPassPassengerName,
      boardingPassFlightNumber,
      boardingPassFlightTime,
      boardingPassOrigin,
      boardingPassDestination,
      boardingPassSeat)
    
    print(cmd)

if (NameValidation == True) and (DoBValidation == True) and PersonValidation == True and BoardingPassValidation == True and LuggageValidation == True:
   cmd ='''
    Dear Mr {},\n
    You are welcome to flight # {} leaving at {} from {} to {}.\n
    Your seat number is {}, and it is confirmed.\n
    We did not find a prohibited item (lighter) in your carry-on baggage.\n
    thanks for following the procedure.\n
    Your identity is verified so please board the plane.'''.format(
      boardingPassPassengerName,
      boardingPassFlightNumber,
      boardingPassFlightTime,
      boardingPassOrigin,
      boardingPassDestination,
      boardingPassSeat)
   print(cmd)