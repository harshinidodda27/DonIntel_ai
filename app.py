import os
from utils.history import save_history

from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
from docx import Document
from PIL import Image
from PyPDF2 import PdfReader


def extract_docx_text(uploaded_file) -> str:
    uploaded_file.seek(0)
    document = Document(uploaded_file)
    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )


st.set_page_config(
    page_title="DocIntel AI",
    page_icon="📄",
    layout="wide",
)

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = None
if api_key:
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

if "processed_file_id" not in st.session_state:
    st.session_state.processed_file_id = ""

if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

if "summary_text" not in st.session_state:
    st.session_state.summary_text = ""

st.title("📄 Enterprise Document Intelligence")
st.write("Upload enterprise documents securely and analyze them using Gemini AI.")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.subheader("🤖 GenAI Connection Test")

if st.button("Test Gemini AI"):
    if not api_key:
        st.error("API key not found. Please check your .env file.")
    else:
        try:
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
        {"role": "user", "content": "Reply with: AI connection is working."}
    ],
)

            st.write(response.choices[0].message.content)
        except Exception as error:
            st.error(
                "Gemini connection failed. Check the API key, internet connection, "
                "or quota and try again."
            )
            with st.expander("Technical details"):
                st.code(str(error))

uploaded_file = st.file_uploader(
    "Choose a document",
    type=["pdf", "png", "jpg", "jpeg", "docx"],
)

if uploaded_file is not None:
    file_id = f"{uploaded_file.name}-{uploaded_file.size}"

    if st.session_state.processed_file_id != file_id:
        st.session_state.processed_file_id = file_id
        st.session_state.extracted_text = ""
        st.session_state.summary_text = ""

    safe_file_name = os.path.basename(uploaded_file.name)
    file_path = os.path.join(UPLOAD_FOLDER, safe_file_name)

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    st.success("✅ File Uploaded Successfully!")

    save_history(uploaded_file.name, uploaded_file.type)

    st.write("### File Details")
    st.write(f"**File Name:** {uploaded_file.name}")
    st.write(f"**File Type:** {uploaded_file.type}")
    st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")

    extracted_text = st.session_state.extracted_text

    if uploaded_file.type == "application/pdf":
        if not extracted_text:
            try:
                uploaded_file.seek(0)
                pdf_reader = PdfReader(uploaded_file)
                pages_text = []

                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pages_text.append(page_text)

                extracted_text = "\n".join(pages_text)
                st.session_state.extracted_text = extracted_text

            except Exception as error:
                st.error("Could not extract text from the PDF.")
                with st.expander("Technical details"):
                    st.code(str(error))
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":

       if not extracted_text:
        try:
            uploaded_file.seek(0)
            extracted_text = extract_docx_text(uploaded_file)
            st.session_state.extracted_text = extracted_text

        except Exception as error:
            st.error("Could not extract text from the DOCX file.")
            with st.expander("Technical details"):
                st.code(str(error))

    elif uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
        try:
            uploaded_file.seek(0)
            image = Image.open(uploaded_file)

            st.image(
                image,
                caption="Uploaded Image",
                use_container_width=True,
            )

            if not extracted_text:
               st.info("Image uploaded successfully.")
               extracted_text = "Image uploaded successfully. (AI image analysis can be added later.)"
               st.session_state.extracted_text = extracted_text
            try:
                     response = client.chat.completions.create(
                        model="openai/gpt-4o-mini",
                        messages=[
            {
                "role": "user",
                "content": f"Summarize the following document in clear and simple points:\n\n{extracted_text}"
            }
        ],
    )

                    st.session_state.summary_text = response.choices[0].message.content

            except Exception as error:
            st.error(f"Summary generation failed: {error}")
        except Exception as error:
            st.error(
                "Image analysis failed. Check your Gemini quota and try again."
            )
            with st.expander("Technical details"):
                st.code(str(error))

    else:
        st.warning("Unsupported file type.")

    extracted_text = st.session_state.extracted_text

    if extracted_text.strip():
        st.subheader("Extracted Text")

        st.text_area(
            "Document Content",
            extracted_text,
            height=300,
        )

        st.subheader("🤖 AI Summary")

        if st.session_state.summary_text:
            if not api_key:
                st.error("API key not found. Please check your .env file.")
            else:
                prompt = f"""
                Summarize the following document in clear and simple points:

                {extracted_text}
                """

                try:
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    response = model.generate_content(prompt)
                    st.session_state.summary_text = response.text
                except Exception as error:
                    st.error(
                        "Summary generation failed. Check your Gemini quota "
                        "and try again."
                    )
                    with st.expander("Technical details"):
                        st.code(str(error))

        if st.session_state.summary_text:
            st.success("✅ Summary Generated Successfully!")
            st.write(st.session_state.summary_text)
            st.download_button(
    label="📥 Download AI Summary",
    data=st.session_state.summary_text,
    file_name="AI_Summary.txt",
    mime="text/plain",
)
    else:
        st.info("No readable text was found in the uploaded file.")
else:
    st.info("Upload a PDF, DOCX, PNG, JPG, or JPEG file to begin.")
