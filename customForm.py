import sys
import os

sys.path.append("/Users/manfrednde/Library/Python/3.9/lib/python/site-packages")

import os
from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import FormTrainingClient
from azure.core.credentials import AzureKeyCredential

AZURE_FORM_RECOGNIZER_ENDPOINT = "https://formrecogniserbaording.cognitiveservices.azure.com/"
AZURE_FORM_RECOGNIZER_KEY = "ad34b28b260a428f8c19e2dd366d0568"

endpoint = AZURE_FORM_RECOGNIZER_ENDPOINT
key = AZURE_FORM_RECOGNIZER_KEY

form_training_client = FormTrainingClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# saved_model_list = form_training_client.list_custom_models()

# trainingDataUrl = "https://stbaordingkiosk.blob.core.windows.net/kiosk-container?sp=rcwd&st=2023-05-30T02:08:46Z&se=2023-07-08T10:08:46Z&sv=2022-11-02&sr=c&sig=p7kyaWu1%2FdBje%2BXTwM6ONHQjU2OBc1MFTJsbY03QwoI%3D"

# training_process = form_training_client.begin_training(trainingDataUrl, use_training_labels=True)
# custom_model = training_process.result()

# custom_model

# custom_model.model_id

# custom_model.status

# custom_model.training_started_on

# custom_model.training_completed_on

# custom_model.training_documents

# for doc in custom_model.training_documents:
#     print("Document name: {}".format(doc.name))
#     print("Document status: {}".format(doc.status))
#     print("Document page count: {}".format(doc.page_count))
#     print("Document errors: {}".format(doc.errors))

# custom_model.properties

# custom_model.submodels

# for submodel in custom_model.submodels:
#     print(
#         "The submodel with form type '{}' has recognized the following fields: {}".format(
#             submodel.form_type,
#             ", ".join(
#                 [
#                     field.label if field.label else name
#                     for name, field in submodel.fields.items()
#                 ]
#             ),
#         )
#     )

# custom_model.model_id



custom_model_info = form_training_client.get_custom_model(model_id="1a8a813a-339c-475b-a438-307bab368d3a")
# custom_model_info = form_training_client.get_custom_model(model_id=custom_model.model_id)
print("Model ID: {}".format(custom_model_info.model_id))
print("Status: {}".format(custom_model_info.status))
print("Training started on: {}".format(custom_model_info.training_started_on))
print("Training completed on: {}".format(custom_model_info.training_completed_on))


# Using an image document as test document URL (Not using PDF here)

new_test_url = "https://stbaordingkiosk.blob.core.windows.net/kiosk-container/boarding-avkash.pdf?sp=rcwd&st=2023-05-30T02:02:41Z&se=2023-07-08T10:02:41Z&sv=2022-11-02&sr=b&sig=WJVy6ScPlpk7%2FnCScaYBYJ5S%2BT80IWw3RTUWz08WXEA%3D"
new_test_url

form_recognizer_client = FormRecognizerClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# custom_model.model_id

custom_model_info.model_id

custom_test_action = form_recognizer_client.begin_recognize_custom_forms_from_url(model_id=custom_model_info.model_id, form_url=new_test_url)

custom_test_action.status()

custom_test_action_result = custom_test_action.result()

for recognized_content in custom_test_action_result:
    print("Form type: {}".format(recognized_content.form_type))
    for name, field in recognized_content.fields.items():
        print("Field '{}' has label '{}' with value '{}' and a confidence score of {}".format(
            name,
            field.label_data.text if field.label_data else name,
            field.value,
            field.confidence
        ))


##


#------------------------------------------

labeled_training_process = form_training_client.begin_training(trainingDataUrl, use_training_labels=True)
labeled_custom_model = labeled_training_process.result()

labeled_custom_model.model_id

labeled_custom_model.status

labeled_custom_model.training_documents

for doc in labeled_custom_model.training_documents:
    print("Document name: {}".format(doc.name))
    print("Document status: {}".format(doc.status))
    print("Document page count: {}".format(doc.page_count))
    print("Document errors: {}".format(doc.errors))

labeled_custom_model.model_id

labeled_custom_test_action = form_recognizer_client.begin_recognize_custom_forms_from_url(model_id=labeled_custom_model.model_id, form_url=new_test_url)

labeled_custom_test_action.status()

labeled_custom_test_action_result = labeled_custom_test_action.result()

for recognized_content in labeled_custom_test_action_result:
    print("Form type: {}".format(recognized_content.form_type))
    for name, field in recognized_content.fields.items():
        print("Field '{}' has label '{}' with value '{}' and a confidence score of {}".format(
            name,
            field.label_data.text if field.label_data else name,
            field.value,
            field.confidence
        ))

saved_model_list = form_training_client.list_custom_models()

for model in saved_model_list:
    print(model.model_id)

