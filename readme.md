# Cruxify AI - Setup Instructions

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Tesseract OCR (for image text extraction)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Tesseract OCR

#### Windows:
1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH

#### Mac:
```bash
brew install tesseract
```

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install tesseract-ocr
```

### 3. Update API Key
Edit the `TOGETHER_API_KEY` in `main.py` with your actual Together AI API key:
```python
os.environ["TOGETHER_API_KEY"] = "YOUR_ACTUAL_API_KEY_HERE"
```

### 4. Run the Application

#### Start FastAPI Backend:
```bash
uvicorn main:app --reload
```
The API will be available at: http://localhost:8000

#### Start Streamlit Frontend:
```bash
streamlit run app.py
```
The web app will be available at: http://localhost:8501

## 📁 Project Structure
```
cruxify-ai/
├── main.py              # FastAPI backend
├── app.py               # Streamlit frontend
├── requirements.txt     # Python dependencies
├── README.md           # Setup instructions
└── logo.png            # App logo (place your logo here)
```

## 🔧 Configuration

### API Endpoints
- `GET /` - Health check
- `POST /summarize/text` - Summarize plain text (JSON)
- `POST /summarize/text/form` - Summarize text (form data)
- `POST /summarize/file` - Summarize file content
- `GET /health` - Service health status

### Supported File Types
- **PDF**: `.pdf`
- **Word Documents**: `.docx`, `.doc`
- **Images**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`

## 🎨 Features

### Text Summarizer
- Input text directly in a text area
- Minimum 50 characters required
- Real-time character counting
- Summary statistics (reduction percentage)

### Image Summarizer
- Upload multiple file types
- OCR text extraction from images
- PDF text extraction
- Word document processing
- File size and type validation

### UI Features
- Responsive sidebar navigation
- Hover animations on buttons and cards
- Modern gradient design
- Contact information
- Contributors section
- Error handling with user-friendly messages

## 🛠️ Troubleshooting

### Common Issues

1. **"Cannot connect to backend"**
   - Ensure FastAPI server is running on port 8000
   - Check if `BACKEND_URL` in app.py matches your FastAPI server

2. **"Tesseract not found"**
   - Install Tesseract OCR and ensure it's in your PATH
   - On Windows, you might need to specify the path in your code

3. **"API Key Error"**
   - Verify your Together AI API key is correct
   - Check if you have sufficient API credits

4. **File Upload Issues**
   - Ensure file size is under 10MB
   - Check if file format is supported
   - Verify the file is not corrupted

## 🎯 Usage Tips

1. **Text Summarization**:
   - Longer texts (500+ words) produce better summaries
   - Technical documents work well with the AI model
   - Clean, well-formatted text gives better results

2. **Image/File Processing**:
   - High-resolution images with clear text work best for OCR
   - PDF files with selectable text are processed faster
   - Scanned documents may take longer to process

3. **Performance**:
   - First API call may be slower due to model loading
   - Subsequent requests are typically faster
   - Large files may take 10-30 seconds to process

## 📝 API Documentation

Once the FastAPI server is running, visit:
- http://localhost:8000/docs - Interactive API documentation
- http://localhost:8000/redoc - Alternative API documentation

## 🔒 Security Notes

- The current setup is for development/testing
- For production deployment:
  - Use environment variables for API keys
  - Implement rate limiting
  - Add authentication if needed
  - Use HTTPS
  - Validate file uploads more strictly