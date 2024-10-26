import boto3
import time

# Initialize AWS services
region = ''
rekognition = boto3.client('rekognition', region_name=region)
s3 = boto3.client('s3', region_name=region)

# Define the bucket name and video file name
bucket_name = '<bucket_name>'
video_name = '<video_file_name>'

# Start content moderation job
start_moderation_label_detection = rekognition.start_content_moderation(
    Video={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': video_name,
        }
    },
)

moderation_job_id = start_moderation_label_detection['JobId']
print("Job Id:", moderation_job_id)

# Wait for content moderation job to complete
while True:
    moderation_job_status = rekognition.get_content_moderation(JobId=moderation_job_id)
    if moderation_job_status['JobStatus'] == 'SUCCEEDED':
        break
    elif moderation_job_status['JobStatus'] == 'FAILED':
        print("Content moderation job failed.")
        break
    else:
        time.sleep(5)  # Wait for 5 seconds before checking job status again

# Get the moderation labels detected in the video
moderation_labels = moderation_job_status.get('ModerationLabels', [])

# Initialize detection flags
explicit_detected = False
suggestive_detected = False
violent_detected = False
alcohol_detected = False
drug_abuse_detected = False
offensive_detected = False
tobacco_detected = False
hate_symbols_detected = False
gambling_detected = False
graphic_content_detected = False
adult_content_detected = False

# Categorize moderation labels
for label in moderation_labels:
    label_name = label['ModerationLabel']['Name']
    if label_name.lower() == 'explicit nudity':
        explicit_detected = True
    elif label_name.lower() == 'suggestive':
        suggestive_detected = True
    elif label_name.lower() == 'violence':
        violent_detected = True
    elif label_name.lower() == 'alcohol':
        alcohol_detected = True
    elif label_name.lower() == 'drug abuse':
        drug_abuse_detected = True
    elif label_name.lower() == 'offensive':
        offensive_detected = True
    elif label_name.lower() == 'tobacco':
        tobacco_detected = True
    elif label_name.lower() == 'hate symbols':
        hate_symbols_detected = True
    elif label_name.lower() == 'gambling':
        gambling_detected = True
    elif label_name.lower() == 'graphic content':
        graphic_content_detected = True
    elif label_name.lower() == 'adult content':
        adult_content_detected = True

# Display detection results
print("Moderation labels detected:")
print(f"Explicit Nudity: {'Detected' if explicit_detected else 'Not Detected'}")
print(f"Suggestive: {'Detected' if suggestive_detected else 'Not Detected'}")
print(f"Violence: {'Detected' if violent_detected else 'Not Detected'}")
print(f"Alcohol: {'Detected' if alcohol_detected else 'Not Detected'}")
print(f"Drug Abuse: {'Detected' if drug_abuse_detected else 'Not Detected'}")
print(f"Offensive: {'Detected' if offensive_detected else 'Not Detected'}")
print(f"Tobacco: {'Detected' if tobacco_detected else 'Not Detected'}")
print(f"Hate Symbols: {'Detected' if hate_symbols_detected else 'Not Detected'}")
print(f"Gambling: {'Detected' if gambling_detected else 'Not Detected'}")
print(f"Graphic Content: {'Detected' if graphic_content_detected else 'Not Detected'}")
print(f"Adult Content: {'Detected' if adult_content_detected else 'Not Detected'}")

# Generate a presigned URL for the video
s3_video_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': video_name})

# Print the video URL
print("Video URL:", s3_video_url)
