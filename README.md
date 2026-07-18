# 📄 Enterprise Document Intelligence

An AI-powered document processing application built using *Streamlit*. The application allows users to upload PDF, DOCX, and image-based documents, extract their content, generate AI-powered summaries, and download the results.

## 🚀 Features

- 📄 Upload PDF documents
- 📝 Upload DOCX documents
- 🖼️ Upload image-based documents (JPG, JPEG, PNG)
- 🔍 Extract text from PDF files
- 📑 Extract text from Word documents
- 🤖 AI-powered document summarization
- 📥 Download generated summaries
- 🎨 Simple and user-friendly Streamlit interface

## 🛠️ Technologies Used

- Python
- Streamlit
- PyPDF2
- python-docx
- Pillow (PIL)
- Google Gemini API
- python-dotenv

## 📂 Project Structure


Enterprise-Document-Intelligence/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── utils/
│   ├── pdf_utils.py
│   ├── docx_utils.py
│   ├── image_utils.py
│   └── ai_utils.py
└── assets/


## ⚙️ Installation

Clone the repository:

bash
git clone https://github.com/yourusername/Enterprise-Document-Intelligence.git


Move into the project folder:

bash
cd Enterprise-Document-Intelligence


Install dependencies:

bash
pip install -r requirements.txt


Create a .env file:


GOOGLE_API_KEY=YOUR_API_KEY


Run the application:

bash
streamlit run app.py


## 📋 Supported File Types

- PDF (.pdf)
- Microsoft Word (.docx)
- Images (.jpg, .jpeg, .png)

## 📌 How It Works

1. Upload a document.
2. The application extracts the document content.
3. AI generates a concise summary.
4. Users can download the generated summary.

## ⚠️ Known Issue

The AI summary feature depends on the availability of the configured Gemini API. If the free-tier quota has been exhausted or is unavailable, summary generation may fail until quota is restored or another supported AI provider is configured.

## 🎯 Future Enhancements

- OCR support for scanned documents
- Multi-language document processing
- Chat with uploaded documents
- Document classification
- Keyword extraction
- Cloud storage integration

## 👨‍💻 Developed For

FlowZint AI Hackathon 2026

---

Made with ❤️ using Python and Streamlit.
