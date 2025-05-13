from flask import Flask, request, jsonify
import pytesseract
from pdf2image import convert_from_path
import os
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)

@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_path = os.path.join(tmpdir, filename)
            file.save(pdf_path)

            try:
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
    else:
        return jsonify({'error': 'Only PDF files are supported'}), 400


if __name__ == '__main__':
    app.run(debug=True)
