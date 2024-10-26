import boto3
import os
import io
import datetime
from IPython.display import HTML, display
import uuid
import json
import time

# Set variables
region = ''
role = "<your_role>"
bucket_name = ''  # Provide your bucket name here
s3_key = '<audio_file_name>'


os.environ["REGION"] = region

print(f"Region is: {region}\nRole is: {role}")

rekognition = boto3.client('rekognition', region_name=region)
comprehend = boto3.client('comprehend', region_name=region)
transcribe = boto3.client('transcribe', region_name=region)
s3 = boto3.client('s3', region_name=region)

video_path = r'<path>'

# Start moderation label detection
startModerationLabelDetection = rekognition.start_content_moderation(
    Video={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': s3_key
        }
    }
)

moderationJobId = startModerationLabelDetection['JobId']
display("Job Id: {0}".format(moderationJobId))

# Get content moderation results
getContentModeration = rekognition.get_content_moderation(
    JobId=moderationJobId,
    SortBy='TIMESTAMP'
)

while getContentModeration['JobStatus'] == 'IN_PROGRESS':
    time.sleep(5)
    print('.', end='')
    getContentModeration = rekognition.get_content_moderation(
        JobId=moderationJobId,
        SortBy='TIMESTAMP'
    )

display(getContentModeration['JobStatus'])

label_html = ''''''
for label in getContentModeration["ModerationLabels"]:
    if len(label["ModerationLabel"]["ParentName"]) > 0:
        label_html += f'''<a onclick="document.getElementById('cccvid1').currentTime={round(label['Timestamp']/1000)}">[{label['Timestamp']} ms]: 
                {label['ModerationLabel']['Name']}, confidence: {round(label['ModerationLabel']['Confidence'],2)}%</a><br/>
                '''
display(HTML(label_html))

# Start text detection
getTextDetection = rekognition.start_text_detection(
    Video={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': s3_key
        }
    }
)

textJobId = getTextDetection['JobId']
display("Job Id: {0}".format(textJobId))

# Get text detection results
getTextDetection = rekognition.get_text_detection(JobId=textJobId)

while getTextDetection['JobStatus'] == 'IN_PROGRESS':
    time.sleep(5)
    print('.', end='')

    getTextDetection = rekognition.get_text_detection(JobId=textJobId)

display(getTextDetection['JobStatus'])

text_html = ''''''
for txt in getTextDetection["TextDetections"]:
    if txt["TextDetection"]["Type"] == 'LINE':
        text_html += f'''<a onclick="document.getElementById('cccvid2').currentTime={round(txt['Timestamp']/1000)}">[{txt['Timestamp']} ms]: 
                {txt["TextDetection"]["DetectedText"]}, confidence: {round(txt["TextDetection"]["Confidence"],2)}%</a><br/>
                '''
display(HTML(text_html))

# Start transcription job
job_name = f'video_moderation_{str(uuid.uuid1())[0:4]}'

transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': f's3://{bucket_name}/{s3_key}'},  # S3 URI to the video
    OutputBucketName='suii',  # Specify your output bucket name here
    OutputKey='transcriptions/output.json',  # Optional: Specify your output key (path) here
    MediaFormat='mp4',
    LanguageCode='en-US'
)


getTranscription = transcribe.get_transcription_job(TranscriptionJobName=job_name)

while getTranscription['TranscriptionJob']['TranscriptionJobStatus'] == 'IN_PROGRESS':
    time.sleep(5)
    print('.', end='')

    getTranscription = transcribe.get_transcription_job(TranscriptionJobName=job_name)

display(getTranscription['TranscriptionJob']['TranscriptionJobStatus'])

filename = f'transcriptions/output.json'
s3_clientobj = boto3.client('s3', region_name=region).get_object(Bucket=bucket_name, Key=filename)
s3_clientdata = s3_clientobj["Body"].read().decode("utf-8")
original = json.loads(s3_clientdata)
output_transcript = original["results"]["transcripts"]
print(output_transcript)
