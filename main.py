from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai
import PyPDF2
import docx
from PIL import Image
import pytesseract
import io
import base64
from typing import Optional



app = FastAPI(title="Cruxify AI API", description="AI-powered text and image summarization API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up Together AI API
os.environ["TOGETHER_API_KEY"] = "0bc66dcded6a57c5aca11ec7f61089f423307023ba560e3b3178fb36c7923a10"

client = openai.OpenAI(
    api_key=os.environ.get("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1",
)

class TextSummaryRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int

def get_summary(text: str) -> str:
    """Get summary using Together AI API"""
    try:
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": "You are a professional summarizer assistant. Provide a concise and informative summary of the given text. Focus on key points and main ideas. Only provide the summary with no additional content."},
                {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
            ],
            max_tokens=500,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting text from PDF: {str(e)}")

def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file"""
    try:
        doc_file = io.BytesIO(file_content)
        doc = docx.Document(doc_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting text from DOCX: {str(e)}")

def extract_text_from_image(file_content: bytes) -> str:
    """Extract text from image using OCR"""
    try:
        image = Image.open(io.BytesIO(file_content))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting text from image: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to Cruxify AI API"}

@app.post("/summarize/text", response_model=SummaryResponse)
async def summarize_text(request: TextSummaryRequest):
    """Summarize plain text input"""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) < 50:
        raise HTTPException(status_code=400, detail="Text too short to summarize (minimum 50 characters)")
    
    summary = get_summary(request.text)
    
    return SummaryResponse(
        summary=summary,
        original_length=len(request.text),
        summary_length=len(summary)
    )

@app.post("/summarize/text/form")
async def summarize_text_form(text: str = Form(...)):
    """Summarize text from form data (for compatibility)"""
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(text) < 50:
        raise HTTPException(status_code=400, detail="Text too short to summarize (minimum 50 characters)")
    
    summary = get_summary(text)
    
    return {
        "Summary": summary,
        "original_length": len(text),
        "summary_length": len(summary)
    }

@app.post("/summarize/file", response_model=SummaryResponse)
async def summarize_file(file: UploadFile = File(...)):
    """Summarize content from uploaded file (PDF, DOCX, or image)"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    file_extension = file.filename.lower().split('.')[-1]
    file_content = await file.read()
    
    # Extract text based on file type
    if file_extension == 'pdf':
        extracted_text = extract_text_from_pdf(file_content)
    elif file_extension in ['docx', 'doc']:
        extracted_text = extract_text_from_docx(file_content)
    elif file_extension in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff']:
        extracted_text = extract_text_from_image(file_content)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF, DOCX, or image files.")
    
    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No text could be extracted from the file")
    
    if len(extracted_text) < 50:
        raise HTTPException(status_code=400, detail="Extracted text too short to summarize")
    
    summary = get_summary(extracted_text)
    
    return SummaryResponse(
        summary=summary,
        original_length=len(extracted_text),
        summary_length=len(summary)
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Cruxify AI API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)