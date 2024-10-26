
import boto3
import sagemaker
from PIL import Image
import io



# variables
role = ""

region = ''  # Set the region to ap-south-1

rekognition = boto3.client('rekognition', region_name=region)
comprehend = boto3.client('comprehend', region_name=region)

print(f"SageMaker role is: {role}")

# Load the image from local directory
local_image_path = r'<image_path>'

with open(local_image_path, 'rb') as f:
    image_bytes = f.read()

# Detect moderation labels
detectModerationLabelsResponse = rekognition.detect_moderation_labels(
    Image={
        'Bytes': image_bytes
    }
)

for label in detectModerationLabelsResponse["ModerationLabels"]:
    print("- {} (Confidence: {})".format(label["Name"], label["Confidence"]))
    print("  - Parent: {}".format(label["ParentName"]))

# Detect text
detectTextResponse = rekognition.detect_text(
    Image={
        'Bytes': image_bytes
    }
)

detected_text_list = []
textDetections = detectTextResponse['TextDetections']
for text in textDetections:
    if text['Type'] == 'LINE':
        print('Detected text: ' + text['DetectedText'])
        detected_text_list.append(text['DetectedText'])

for text in detected_text_list:
    response = comprehend.detect_pii_entities(Text=text, LanguageCode='en')
    if len(response['Entities']) > 0:
        print("Detected PII entity is: " + text[
                                           response['Entities'][0]['BeginOffset']:response['Entities'][0]['EndOffset']])
        print("PII type is: " + response['Entities'][0]['Type'])
        print("Confidence score is: " + str(response['Entities'][0]['Score']))
print()
