from flask import Flask, render_template, send_file
import boto3
from botocore.exceptions import NoCredentialsError
from secret import access_key, secret_access_key

app = Flask(__name__)


s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)


S3_BUCKET = 'medical-reports-ssip'

@app.route('/')
def list_reports():
    try:

        response = s3.list_objects(Bucket=S3_BUCKET)

        if 'Contents' in response:
            reports = [obj['Key'] for obj in response['Contents']]
        else:
            reports = []

        return render_template('list.html', reports=reports)
    except NoCredentialsError:
        return "AWS credentials not available."
    except Exception as e:
        print("Error listing S3 objects:", str(e))
        return "An error occurred while listing S3 objects."

@app.route('/download_report/<filename>')
def download_report(filename):
    try:

        s3.download_file(S3_BUCKET, filename, 'downloaded_report.pdf')

        return send_file('downloaded_report.pdf', as_attachment=True)
    except NoCredentialsError:
        return "AWS credentials not available."

if __name__ == '__main__':
    app.run(debug=True)
