import streamlit as st
from PIL import Image
import pytesseract
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load NLLB-200 model
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def translate_nllb(text, src_lang="eng_Latn", tgt_lang="tel_Telu"):
    """Function to translate English text to Telugu using NLLB-200."""
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang))
    translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
    return translated_text

def extract_text_from_image(image):
    """Extract English text from an image using OCR."""
    extracted_text = pytesseract.image_to_string(image, lang="eng")  # Extract text
    return extracted_text.strip()  # Remove extra spaces and newlines

# Initialize session state for clearing inputs
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = None
if "translated_text" not in st.session_state:
    st.session_state.translated_text = None

# Streamlit UI
st.title("📷 Image Text Translator: English to Telugu 🌍")

# Upload Image
uploaded_file = st.file_uploader("Upload an image with English text", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.session_state.uploaded_file = uploaded_file
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Extract text from image
    with st.spinner("Extracting text..."):
        st.session_state.extracted_text = extract_text_from_image(image)

    if st.session_state.extracted_text:
        st.subheader("Extracted English Text:")
        st.write(f"**{st.session_state.extracted_text}**")

        # Translate to Telugu
        with st.spinner("Translating to Telugu..."):
            st.session_state.translated_text = translate_nllb(st.session_state.extracted_text)

        st.subheader("Translated Telugu Text:")
        st.write(f"**{st.session_state.translated_text}**")
    else:
        st.warning("No text found in the image. Try another one.")

# Reset button to clear previous inputs
if st.button("🔄 Reset"):
    st.session_state.uploaded_file = None
    st.session_state.extracted_text = None
    st.session_state.translated_text = None
    st.experimental_rerun()  # Refresh the page to reset inputs
