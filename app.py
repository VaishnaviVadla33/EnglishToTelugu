import streamlit as st
from PIL import Image, UnidentifiedImageError
import pytesseract
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from gtts import gTTS
import io
import pyperclip  # For clipboard functionality

# Error handling for imports
try:
    # Import rerun (for Streamlit >=1.27)
    try:
        from streamlit.runtime.scriptrunner import rerun
    except ImportError:
        rerun = lambda: None  # fallback if not available

    # Load NLLB-200 model
    model_name = "facebook/nllb-200-distilled-600M"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
except Exception as e:
    st.error(f"Error loading models: {str(e)}")
    st.stop()

# Supported Indian languages in NLLB-200
INDIAN_LANGUAGES = {
    "Telugu": "tel_Telu",
    "Hindi": "hin_Deva",
    "Kannada": "kan_Knda",
    "Tamil": "tam_Taml",
    "Bengali": "ben_Beng",
    "Malayalam": "mal_Mlym",
    "Marathi": "mar_Deva"
}

# Language code for gTTS
GTTS_LANG_CODES = {
    "Telugu": "te",
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Bengali": "bn",
    "Malayalam": "ml",
    "Marathi": "mr"
}

def translate_nllb(text, tgt_lang="tel_Telu"):
    try:
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs, forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_lang))
        translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
        return translated_text
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return ""

def extract_text_from_image(image):
    try:
        extracted_text = pytesseract.image_to_string(image, lang="eng")
        return extracted_text.strip()
    except Exception as e:
        st.error(f"Text extraction error: {str(e)}")
        return ""

def text_to_speech(text, lang='te'):
    try:
        tts = gTTS(text, lang=lang)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        st.error(f"Audio generation error: {str(e)}")
        return None

# Initialize session state
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "results" not in st.session_state:
    st.session_state.results = []

# Page config
st.set_page_config(
    page_title="📷 Multi-Image Translator", 
    page_icon="🌍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .title-text {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 30px;
    }
    .language-selector {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .file-uploader {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .result-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .button-primary {
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 8px !important;
    }
    .button-secondary {
        background-color: #6c757d !important;
        color: white !important;
        border-radius: 8px !important;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #6c757d;
        font-size: 14px;
    }
    .divider {
        border-top: 1px solid #dee2e6;
        margin: 20px 0;
    }
    .translation-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: #000000;  /* Ensure text is black */
    }
    .error-box {
        background-color: #ffebee;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: #000000;  /* Ensure text is black */
    }
    .extracted-text {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: #000000;  /* Ensure text is black */
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown("""
<div class="title-text">
    <h1>📷 Multi-Image Text Translator</h1>
    <p style="color: #7f8c8d; font-size: 16px;">Extract text from images and translate to Indian languages</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🌐 Settings")
    target_lang = st.selectbox(
        "Select target language", 
        list(INDIAN_LANGUAGES.keys()), 
        index=0,
        key="lang_select"
    )
    tgt_lang_code = INDIAN_LANGUAGES[target_lang]
    gtts_lang = GTTS_LANG_CODES.get(target_lang, 'en')
    
    st.markdown("---")
    st.markdown("### How to use:")
    st.markdown("""
    1. Upload one or more images containing English text
    2. The app will automatically extract and translate the text
    3. View results and use the available tools:
       - Download translations
       - Copy to clipboard
       - Listen to audio
    """)
    
    st.markdown("---")
    st.markdown("### Supported Languages:")
    for lang in INDIAN_LANGUAGES:
        st.markdown(f"- {lang}")

# Main content
st.markdown("## 📤 Upload Images")
uploaded_files = st.file_uploader(
    "Drag and drop or click to upload images (PNG, JPG, JPEG)", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True,
    key="file_uploader"
)

if uploaded_files:
    st.session_state.uploaded_files = uploaded_files
    st.session_state.results = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, uploaded_file in enumerate(uploaded_files):
        progress = (i + 1) / len(uploaded_files)
        progress_bar.progress(progress)
        status_text.text(f"Processing {i+1} of {len(uploaded_files)}: {uploaded_file.name}")
        
        try:
            image = Image.open(uploaded_file)
            
            # Resize image for display while maintaining aspect ratio
            max_size = (600, 600)
            image.thumbnail(max_size)
            
            extracted_text = extract_text_from_image(image)
            
            if extracted_text:
                with st.spinner(f"Translating to {target_lang}..."):
                    translated_text = translate_nllb(extracted_text, tgt_lang_code)
                
                st.session_state.results.append({
                    "image": image,
                    "filename": uploaded_file.name,
                    "extracted": extracted_text,
                    "translated": translated_text
                })
            else:
                st.session_state.results.append({
                    "image": image,
                    "filename": uploaded_file.name,
                    "extracted": "No text found in the image",
                    "translated": ""
                })
        except UnidentifiedImageError:
            st.session_state.results.append({
                "image": None,
                "filename": uploaded_file.name,
                "extracted": "Invalid image file",
                "translated": ""
            })
        except Exception as e:
            st.session_state.results.append({
                "image": None,
                "filename": uploaded_file.name,
                "extracted": f"Error processing file: {str(e)}",
                "translated": ""
            })
    
    progress_bar.empty()
    status_text.empty()

# Display results
if st.session_state.results:
    st.markdown("## 📊 Results")
    st.markdown(f"Showing {len(st.session_state.results)} processed images")
    
    for i, res in enumerate(st.session_state.results):
        with st.container():
            st.markdown(f"### 📄 {res['filename']}")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if res["image"]:
                    st.image(res["image"], use_column_width=True)
                else:
                    st.warning("No image preview available")
            
            with col2:
                st.markdown("**Extracted English Text:**")
                if res.get("extracted") and res["extracted"] != "No text found in the image":
                    st.markdown(f'<div class="extracted-text">{res["extracted"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-box">⚠️ No text could be extracted from this image</div>', unsafe_allow_html=True)
                
                if res.get("translated"):
                    st.markdown(f"**Translated {target_lang} Text:**")
                    st.markdown(f'<div class="translation-box">{res["translated"]}</div>', unsafe_allow_html=True)
                    
                    # Action buttons
                    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
                    
                    with btn_col1:
                        st.download_button(
                            label="💾 Download",
                            data=res["translated"],
                            file_name=f"translated_{res['filename'].split('.')[0]}_{target_lang.lower()}.txt",
                            mime="text/plain",
                            key=f"download_{i}",
                            use_container_width=True
                        )
                    
                    with btn_col2:
                        if st.button(
                            "📋 Copy",
                            key=f"copy_{i}",
                            use_container_width=True
                        ):
                            try:
                                pyperclip.copy(res["translated"])
                                st.success("Copied to clipboard!")
                            except Exception as e:
                                st.error(f"Failed to copy: {str(e)}")
                    
                    with btn_col3:
                        with st.spinner("Preparing audio..."):
                            audio_fp = text_to_speech(res["translated"], gtts_lang)
                            if audio_fp:
                                st.audio(audio_fp, format="audio/mp3")
                            else:
                                st.error("Audio generation failed")
                elif res.get("extracted") and res["extracted"] != "No text found in the image":
                    st.warning("Translation failed or no text to translate")
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Reset button
if st.session_state.results or st.session_state.uploaded_files:
    st.markdown("---")
    if st.button("🔄 Reset All", type="primary", use_container_width=True):
        st.session_state.uploaded_files = []
        st.session_state.results = []
        st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Made using Streamlit, Pytesseract, NLLB-200, and gTTS</p>
    <p>Developed by Vaishnavi | © 2025</p>
</div>
""", unsafe_allow_html=True)
