import pytesseract
from pdf2image import convert_from_path
import os

def extract_text_from_pdf(pdf_path):
    # Convert PDF to a list of images
    print("📄 Converting PDF pages to images...")
    images = convert_from_path(pdf_path, dpi=300)

    full_text = ""

    for i, image in enumerate(images):
        print(f"🔍 Running OCR on page {i + 1}...")
        text = pytesseract.image_to_string(image, lang='eng')
        full_text += f"\n\n--- Page {i + 1} ---\n{text}"

    return full_text

if __name__ == "__main__":
    pdf_file = "sample.pdf"  # Change to your PDF path
    if not os.path.exists(pdf_file):
        print(f"❌ File not found: {pdf_file}")
    else:
        text_output = extract_text_from_pdf(pdf_file)
        print("\n✅ Extracted Text:\n")
        print(text_output)

