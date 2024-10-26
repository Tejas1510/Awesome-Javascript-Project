from flask import Flask, request, jsonify, render_template
import boto3
import io
from fpdf import FPDF
from secret import access_key, secret_access_key

app = Flask(__name__)


s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)


S3_BUCKET = 'medical-reports-ssip'

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Medical Report', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def medical_data(self, data):
        self.set_font('Arial', '', 12)
        for key, value in data.items():
            if key == "medicines":
                self.chapter_title("Medicines")
                for medicine in value:
                    self.cell(0, 10, f"Prescription: {medicine['medicine-prescription']}", 0, 1)
                    self.cell(0, 10, f"Medication Timing: {medicine['medication-timing']}", 0, 1)
            else:
                self.cell(0, 10, f"{key.capitalize()}: {value}", 0, 1)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()

        if data:
            pdf = PDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.medical_data(data)


            pdf_file = 'medical_report.pdf'
            pdf.output(pdf_file)


            try:
                s3.upload_file(pdf_file, S3_BUCKET, 'demo.pdf', ExtraArgs={'ContentType': 'application/pdf'})
                return jsonify({"message": "PDF file uploaded to S3 successfully."})
            except Exception as e:
                return jsonify({"error": f"Failed to upload the PDF to S3: {str(e)}"})
        else:
            return jsonify({"error": "No JSON data received."})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
