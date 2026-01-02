import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2 as pdf

# 1. Load environment variables
load_dotenv()

# 2. Configure Gemini API
# Make sure your .env file has GEMINI_API_KEY=...
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("API Key not found. Please check your .env file.")
else:
    genai.configure(api_key=api_key)

# 3. Streamlit Page Config
st.set_page_config(page_title='AI Profile Enhancer', page_icon='📄', layout='centered')

st.title('AI Profile Enhancer')
st.markdown('### Upload your resume to get feedback')

# 4. Inputs
job_role = st.text_input('Enter the role you are applying for', placeholder="e.g. Data Scientist")
uploaded_file = st.file_uploader('Upload your resume', type=['pdf', 'txt'])

analyze = st.button('Analyze Resume')

# 5. Helper function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        reader = pdf.PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
    return text

# 6. Main Logic
if analyze:
    if uploaded_file is not None and job_role:
        try:
            with st.spinner('Analyzing your profile...'):
                # Step A: Extract Text based on file type
                input_text = ""
                if uploaded_file.name.endswith(".pdf"):
                    input_text = extract_text_from_pdf(uploaded_file)
                elif uploaded_file.name.endswith(".txt"):
                    input_text = str(uploaded_file.read(), "utf-8")
                
                # Step B: Create the Prompt
                prompt = f"""
                Act as an expert Technical Recruiter. 
                I am applying for the role of: {job_role}.
                
                Review the following resume text:
                {input_text}
                
                Please provide:
                1. A match percentage for this specific role.
                2. Key strengths in my profile.
                3. Missing keywords or skills that are critical for {job_role}.
                4. Specific recommendations to improve the resume.
                """

                # Step C: Call Gemini
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(prompt)

                # Step D: Display Result
                st.subheader("Analysis Result")
                st.write(response.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload a resume and specify a job role.")