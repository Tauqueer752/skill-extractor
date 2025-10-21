import streamlit as st
import PyPDF2
import docx
from extractor import extract_skills

st.set_page_config(page_title="Smart Skill Extractor", page_icon="🧠", layout="centered")

st.title("🧠 Smart Resume Skill Extractor")
st.write("Upload your resume (PDF or DOCX) to automatically extract your technical skills.")

uploaded_file = st.file_uploader("📁 Upload Resume", type=["pdf", "docx"])

def extract_text_from_pdf(file):
    text = ""
    pdf = PyPDF2.PdfReader(file)
    for page in pdf.pages:
        text += page.extract_text() + " "
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return " ".join([para.text for para in doc.paragraphs])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_docx(uploaded_file)

    if st.button("🔍 Extract Skills"):
        skills = extract_skills(text)
        if skills:
            st.success("✅ Extracted Skills:")
            st.write(", ".join(skills))
        else:
            st.warning("No technical skills detected. Try another file or update skill list.")
else:
    st.info("Please upload a PDF or DOCX resume to begin.")
