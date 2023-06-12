import sys
import os
import json

sys.path.append("/Users/manfrednde/Library/Python/3.9/lib/python/site-packages")

import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

import os, time, uuid

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials

def show_image_in_cell(img_url):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    plt.figure(figsize=(20,10))
    plt.imshow(img)
    plt.show()

TRAINING_ENDPOINT = "https://customvisionboardingkiosk.cognitiveservices.azure.com"
training_key = "cc665eb582794c84ae65e45209c6b243"
training_resource_id = '/subscriptions/1d697ec8-0d3c-4a0f-b9b2-a422ba575a26/resourceGroups/rg-boarding-kiosk/providers/Microsoft.CognitiveServices/accounts/customvisionboardingkiosk'

PREDICTION_ENDPOINT = 'https://customvisionboardingkiosk-prediction.cognitiveservices.azure.com'
prediction_key = "0092025e801246bea8129015b03dd65e"
prediction_resource_id = "/subscriptions/1d697ec8-0d3c-4a0f-b9b2-a422ba575a26/resourceGroups/rg-boarding-kiosk/providers/Microsoft.CognitiveServices/accounts/customvisionboardingkiosk-Prediction"

# Instantiate and authenticate the training client with endpoint and key
training_credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(TRAINING_ENDPOINT, training_credentials)
trainer.api_version

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(PREDICTION_ENDPOINT, prediction_credentials)
predictor.api_version

# Find the object detection domain
# obj_detection_domain = next(domain for domain in trainer.get_domains() if domain.type == "ObjectDetection" and domain.name == "General")

# # Todo: create a new project
# print ("Your Object Detection Training project has been created. Please move on.")
# project_name = uuid.uuid4()
# project = trainer.create_project(project_name, domain_id=obj_detection_domain)

project = {
    "id": "86ccd036-c32e-4fb1-92f6-a74b865d7482"
}



# # Getting Project Details as collective information
# project.as_dict()

# project.status

# # Todo: add tags based on training requirements 
# tag_1 = trainer.create_tag(project["id"], "lighter")



# iteration = trainer.train_project(project["id"])


# # We will keep checking every 10 seconds during the training progress
# while (iteration.status != "Completed"):
#     iteration = trainer.get_iteration(project["id"], iteration.id)
#     print ("Training status: " + iteration.status)
#     print ("Waiting 10 seconds...")
#     time.sleep(10)

# iteration.as_dict()

# iteration_list = trainer.get_iterations(project["id"])
# for iteration_item in iteration_list:
#     print(iteration_item)

# # Todo: check the preformance
# model_perf = trainer.get_iteration_performance(project["id"], iteration_list[0].id)

# model_perf.as_dict()


# # Todo: set the Iteration Name.
publish_iteration_name = "first-iteration-classes-object-detection-custom"
publish_iteration_name = "Iteration2"

# # Todo: publish it to the project endpoint
# trainer.publish_iteration(project["id"], iteration.id, publish_iteration_name, prediction_resource_id)
# print ("Done!")


# Todo: set the right local path
local_image_path = '/Users/manfrednde/softwareDevProjects/cd0461-building-computer-vision-solutions-with-azure-project-starter/starter/lighter_images/'

# Todo: define a perform_prediction function
def perform_prediction(image_file_name):
    with open(os.path.join (local_image_path,  image_file_name), "rb") as image_contents:
       # Todo: set predict object for object detection
        results = predictor.detect_image(project["id"], publish_iteration_name, image_contents.read())
        # Display the results.
        for prediction in results.predictions:
            print("\t" + prediction.tag_name +
                  ": {0:.2f}%".format(prediction.probability * 100))
            

# Todo: upload a test image and set the name of your own image
file_name = 'lighter-31879_1280.png'

perform_prediction(file_name)

# Checking the Image
with open(os.path.join (local_image_path, file_name), 'rb') as img_code:
    img_view_ready = Image.open(img_code)
    plt.figure()
    plt.imshow(img_view_ready)

# Todo: upload another test image and set the name of your own image
file_name_2 = 'lighter-34026_1280.png'

perform_prediction(file_name_2)

# Checking the Image
with open(os.path.join (local_image_path, file_name_2), 'rb') as img_code:
    img_view_ready = Image.open(img_code)
    plt.figure()
    plt.imshow(img_view_ready)

file_name_3 = 'lighter-2113204_1920.jpg'

perform_prediction(file_name_3)

# Checking the Image
with open(os.path.join (local_image_path, file_name_3), 'rb') as img_code:
    img_view_ready = Image.open(img_code)
    plt.figure()
    plt.imshow(img_view_ready)

file_name_4 = 'lighter001.png'

perform_prediction(file_name_4)

# Checking the Image
with open(os.path.join (local_image_path, file_name_4), 'rb') as img_code:
    img_view_ready = Image.open(img_code)
    plt.figure()
    plt.imshow(img_view_ready)

file_name_5 = 'burn-3509496_1920.jpg'

perform_prediction(file_name_5)

# Checking the Image
with open(os.path.join (local_image_path, file_name_5), 'rb') as img_code:
    img_view_ready = Image.open(img_code)
    plt.figure()
    plt.imshow(img_view_ready)

# Todo: set the platform and flavor
platform = "TensorFlow"
flavor = "TensorFlowLite"

# Todo: set the export_iteration method
# export_process = trainer.export_iteration(project["id"], "iteration.id", platform, flavor, raw=True)
export_process = trainer.export_iteration(project["id"], "de02ad14-f4e6-48e5-9fb7-60b04784097c", platform, flavor, raw=True)

# print(export_process.output)

# print(export_process.output.status)

# Code snippet is from Azure SDK and Documentation
# https://docs.microsoft.com/en-us/azure/cognitive-services/custom-vision-service/export-programmatically
# This step may take long time 
while (export_process.output.status == "Exporting"):
    print ("Waiting 10 seconds...")
    time.sleep(10)
    #exports = trainer.get_exports(project_id, selected_iteration_id)
    exports = trainer.get_exports(project["id"],"de02ad14-f4e6-48e5-9fb7-60b04784097c")
    for e in exports:
        if e.platform == export_process.output.platform and e.flavor == export_process.output.flavor:
            export = e
            break
    print("Export status is: ", export_process.output.status)

print(export_process.output.status)

print(export_process.output.download_uri)

# Downloading the model from url.
if export_process.output.status == "Done":
    # Ready to Download
    model_export_file = requests.get(export_process.output.download_uri)
    # You can set the name of the download file here
    with open("trained-model.zip", "wb") as file:
        file.write(model_export_file.content)