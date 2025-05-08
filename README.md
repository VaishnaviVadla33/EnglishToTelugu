# 📷 Image Text Translator: English to Telugu 🌍

A web-based app that extracts English text from images using OCR and translates it into Telugu using Meta’s NLLB-200 multilingual model.

---

## 🚀 Features

✅ Upload English text images (png, jpg, jpeg)  
✅ Extract text using Tesseract OCR  
✅ Translate English to Telugu using NLLB-200 (distilled 600M model)  
✅ Interactive Streamlit interface  
✅ Reset button to clear uploaded files and results  
✅ Fast, lightweight, and easy to use!

---

## 🔧 Technologies Used

- **Python 3.8+**
- **Streamlit** → Web UI
- **Pillow (PIL)** → Image processing
- **pytesseract** → Optical Character Recognition
- **Transformers + NLLB-200** → Multilingual translation
- **Torch** → Backend for transformers

---

## 📦 Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/VaishnaviVadla33/EnglishToTelugu.git
    cd EnglishToTelugu
    ```

2. **Set up a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Install Tesseract OCR**
    - **Ubuntu:** `sudo apt-get install tesseract-ocr`
    - **Windows:** Download from [Tesseract releases](https://github.com/tesseract-ocr/tesseract/wiki)

---

## 💻 Running the App

```bash
streamlit run app.py
