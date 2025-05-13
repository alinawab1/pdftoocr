from flask import Flask, request, jsonify
import pytesseract
from pdf2image import convert_from_path
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

        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = os.path.join(tmpdir, "uploaded.pdf")

            # Write PDF bytes to a file
            with open(pdf_path, 'wb') as f:
                f.write(pdf_bytes)

            print("📄 Converting PDF pages to images...")
            images = convert_from_path(pdf_path, dpi=300)

            full_text = ""
            for i, image in enumerate(images):
                print(f"🔍 Running OCR on page {i + 1}...")
                text = pytesseract.image_to_string(image, lang='eng')
                full_text += f"\n\n--- Page {i + 1} ---\n{text}"

            return jsonify({'text': full_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Render requires binding to 0.0.0.0 and using the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

