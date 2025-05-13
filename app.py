from flask import Flask, request, jsonify
import pytesseract
from pdf2image import convert_from_bytes
import base64
import os
import tempfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/extract-text', methods=['POST'])
def extract_text():
    data = request.get_json()

    if not data or 'pdf_base64' not in data:
        return jsonify({'error': 'Missing "pdf_base64" in request body'}), 400

    try:
        # Decode base64 string to binary PDF data
        pdf_bytes = base64.b64decode(data['pdf_base64'])

        # Convert PDF pages to images at lower DPI (150)
        images = convert_from_bytes(pdf_bytes, dpi=150)

        # Run OCR on each page
        full_text = ""
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang='eng')
            full_text += f"\n\n--- Page {i + 1} ---\n{text}"

        return jsonify({'text': full_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/echo-string', methods=['POST'])
def echo_string():
    data = request.get_json()
    if not data or 'input' not in data:
        return jsonify({'error': 'Missing "input" in request body'}), 400
    return jsonify({'output': data['input']})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
