# Cloud Storage Demo

This project demonstrates a simple cloud storage setup where users can upload and list PDF files stored on the cloud.

## Prerequisites

Before executing the program, make sure you have:

- **An IDE**: VS Code, PyCharm, or any other IDE to run Python programs.

## Steps to Execute the Program

### 1. Upload (For 1 Demo Test)

1. Open the `Cloud Storage` folder in your IDE.
2. In the terminal, run the `upload.py` file.
3. You should see an output indicating the localhost address (e.g., `* Running on http://127.0.0.1:5000`).
4. Follow the link in your browser.
5. Fill in dummy details for the test.
6. Click the **Submit** button.
7. You will receive a notification message: `'PDF file uploaded to S3 successfully'`.
8. **Note**: If you want to upload again, you must change the file name in the code manually to prevent overwriting the previous file.

### 2. List

1. Open the `Cloud Storage` folder in your IDE.
2. In the terminal, run the `list.py` file.
3. You should see an output indicating the localhost address (e.g., `* Running on http://127.0.0.1:5000`).
4. Follow the link in your browser.
5. You will see the uploaded PDF file (this displays all files uploaded to the cloud; for this demo, you’ll see only one).
6. Click on the file name to download the PDF file to your system.
7. Verify the content to ensure it matches what was uploaded to the cloud.

## Notes

- For this demo, only one file is shown; however, this setup generally supports multiple files on the cloud.
