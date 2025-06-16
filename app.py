import streamlit as st
import requests
import json
from PIL import Image
import base64
import io
import os

# Page configuration
st.set_page_config(
    page_title="Cruxify AI",
    page_icon="assets/logo.png",  # or "assets/favicon.png"
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for styling and animations
st.markdown("""
<style>
    .main-header {
        text-align: center;
        font-size: 3.5rem;
        font-weight: bold;
        color: #2E8B57;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .welcome-text {
        text-align: center;
        font-size: 1.5rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.2);
    }
    
    .feature-title {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .feature-description {
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .sidebar-header {
        color: #2E8B57;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .contact-info {
        background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    
    .contributors-section {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    
    .summary-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2E8B57;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #fff5f5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #e53e3e;
        color: #e53e3e;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #f0fff4;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #38a169;
        color: #38a169;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(46, 139, 87, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 139, 87, 0.4);
    }
    
    .logo-container {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# FastAPI backend URL (adjust as needed)
BACKEND_URL = "http://127.0.0.1:8000"

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Function to load and encode logo
@st.cache_data
def load_logo():
    """Load logo image and convert to base64 for embedding"""
    logo_paths = [
        "logo.png",
        "assets/logo.png", 
        "images/logo.png",
        "static/logo.png"
    ]
    
    for path in logo_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    return base64.b64encode(f.read()).decode()
            except Exception as e:
                st.error(f"Error loading logo from {path}: {e}")
                continue
    
    return None

# Load logo
logo_base64 = load_logo()

# Sidebar
with st.sidebar:
    # Logo in sidebar
    if logo_base64:
        st.markdown(f'''
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <img src="data:image/png;base64,{logo_base64}" width="80" style="border-radius: 10px;">
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-header">🧠 Cruxify AI</div>', unsafe_allow_html=True)
    
    # Navigation
    st.markdown("### 🚀 Features")
    
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.current_page = 'home'
    
    if st.button("📝 Text Summarizer", use_container_width=True):
        st.session_state.current_page = 'text_summarizer'
    
    if st.button("🖼️ Image Summarizer", use_container_width=True):
        st.session_state.current_page = 'image_summarizer'
    
    st.markdown("---")
    
    # Contact Us
    st.markdown("""
    <div class="contact-info">
        <h4>📧 Contact Us</h4>
        <p>Email: akhileshcodes.tech@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contributors
    st.markdown("""
    <div class="contributors-section">
        <h4>👥 Contributors</h4>
        <ul>
            <li>Akhilesh</li>
            <li>Pratham</li>
            <li>Diljit</li>
            <li>Bavika</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main content area
def show_home():
    # Logo at the top of main page
    if logo_base64:
        st.markdown(f'''
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" width="120" style="border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        </div>
        ''', unsafe_allow_html=True)
    else:
        # Fallback emoji if logo not found
        st.markdown('<div class="logo-container">🧠</div>', unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">Cruxify AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-text">Welcome User!</p>', unsafe_allow_html=True)
    
    # Feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📝 Text Summarizer</div>
            <div class="feature-description">
                Transform lengthy texts into concise, meaningful summaries. 
                Perfect for articles, documents, and research papers.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Launch Text Summarizer", key="text_sum_home", use_container_width=True):
            st.session_state.current_page = 'text_summarizer'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🖼️ Image Summarizer</div>
            <div class="feature-description">
                Extract and summarize text from images, PDFs, and documents. 
                Supports multiple file formats with OCR technology.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Launch Image Summarizer", key="img_sum_home", use_container_width=True):
            st.session_state.current_page = 'image_summarizer'
            st.rerun()

def show_text_summarizer():
    st.title("📝 Text Summarizer")
    st.markdown("Enter your text below and get an AI-powered summary instantly!")
    
    # Text input
    user_text = st.text_area(
        "Enter text to summarize:",
        height=200,
        placeholder="Paste your text here... (minimum 50 characters)"
    )
    
    # Character count
    char_count = len(user_text)
    st.write(f"Character count: {char_count}")
    
    if char_count < 50 and char_count > 0:
        st.markdown('<div class="error-box">⚠️ Text must be at least 50 characters long</div>', unsafe_allow_html=True)
    
    # Summarize button
    if st.button("🚀 Summarize Text", disabled=(char_count < 50)):
        if user_text.strip():
            with st.spinner("Generating summary..."):
                try:
                    # Make API request
                    response = requests.post(
                        f"{BACKEND_URL}/summarize/text/form",
                        data={"text": user_text}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.markdown('<div class="success-box">✅ Summary generated successfully!</div>', unsafe_allow_html=True)
                        
                        # Display summary
                        st.markdown(f"""
                        <div class="summary-box">
                            <h4>📋 Summary</h4>
                            <p>{result['Summary']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Statistics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Original Length", f"{result.get('original_length', len(user_text))} chars")
                        with col2:
                            st.metric("Summary Length", f"{result.get('summary_length', len(result['Summary']))} chars")
                        with col3:
                            reduction = ((len(user_text) - len(result['Summary'])) / len(user_text)) * 100
                            st.metric("Reduction", f"{reduction:.1f}%")
                        
                    else:
                        st.markdown(f'<div class="error-box">❌ Error: {response.json().get("detail", "Unknown error")}</div>', unsafe_allow_html=True)
                        
                except requests.exceptions.ConnectionError:
                    st.markdown('<div class="error-box">❌ Cannot connect to the backend. Please make sure the FastAPI server is running.</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Unexpected error: {str(e)}</div>', unsafe_allow_html=True)

def show_image_summarizer():
    st.title("🖼️ Image Summarizer")
    st.markdown("Upload PDFs, Word documents, or images to extract and summarize text!")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'docx', 'doc', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'],
        help="Supported formats: PDF, DOCX, DOC, PNG, JPG, JPEG, GIF, BMP, TIFF"
    )
    
    if uploaded_file is not None:
        # File info
        st.write(f"**File:** {uploaded_file.name}")
        st.write(f"**Size:** {uploaded_file.size} bytes")
        st.write(f"**Type:** {uploaded_file.type}")
        
        # Process file button
        if st.button("🔍 Extract & Summarize"):
            with st.spinner("Processing file and generating summary..."):
                try:
                    # Prepare file for API request
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    
                    # Make API request
                    response = requests.post(
                        f"{BACKEND_URL}/summarize/file",
                        files=files
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.markdown('<div class="success-box">✅ File processed and summary generated successfully!</div>', unsafe_allow_html=True)
                        
                        # Display summary
                        st.markdown(f"""
                        <div class="summary-box">
                            <h4>📋 Summary</h4>
                            <p>{result['summary']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Statistics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Original Length", f"{result['original_length']} chars")
                        with col2:
                            st.metric("Summary Length", f"{result['summary_length']} chars")
                        with col3:
                            reduction = ((result['original_length'] - result['summary_length']) / result['original_length']) * 100
                            st.metric("Reduction", f"{reduction:.1f}%")
                        
                    else:
                        error_msg = response.json().get("detail", "Unknown error")
                        st.markdown(f'<div class="error-box">❌ Error: {error_msg}</div>', unsafe_allow_html=True)
                        
                except requests.exceptions.ConnectionError:
                    st.markdown('<div class="error-box">❌ Cannot connect to the backend. Please make sure the FastAPI server is running.</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="error-box">❌ Unexpected error: {str(e)}</div>', unsafe_allow_html=True)
    
    # Instructions
    st.markdown("---")
    st.markdown("""
    ### 📋 Instructions:
    1. **PDF Files**: Extract text from PDF documents
    2. **Word Documents**: Process DOCX and DOC files
    3. **Images**: Use OCR to extract text from images (PNG, JPG, JPEG, GIF, BMP, TIFF)
    4. **File Size**: Keep files under 10MB for optimal performance
    5. **Text Quality**: Ensure images have clear, readable text for best OCR results
    """)

# Route to appropriate page
if st.session_state.current_page == 'home':
    show_home()
elif st.session_state.current_page == 'text_summarizer':
    show_text_summarizer()
elif st.session_state.current_page == 'image_summarizer':
    show_image_summarizer()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p> Cruxify AI - Powered by Advanced AI Technology</p>
    <p>Built by Cruxify team</p>
</div>
""", unsafe_allow_html=True)