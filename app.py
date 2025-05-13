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
            images = convert_from_path(pdf_path, dpi=200)  # Lower DPI = faster

            full_text = ""
            custom_config = r'--oem 1 --psm 3'  # Tesseract config for speed

            for i, image in enumerate(images):
                print(f"🔍 Running OCR on page {i + 1}...")

                gray_image = image.convert('L')  # Convert to grayscale for faster OCR
                text = pytesseract.image_to_string(gray_image, lang='eng', config=custom_config)
                full_text += f"\n\n--- Page {i + 1} ---\n{text}"

            return jsonify({'text': full_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 🔁 Simple echo endpoint for testing
@app.route('/echo-string', methods=['POST'])
def echo_string():
    data = request.get_json()

    if not data or 'input' not in data:
        return jsonify({'error': 'Missing "input" in request body'}), 400

    return jsonify({'output': data['input']})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
