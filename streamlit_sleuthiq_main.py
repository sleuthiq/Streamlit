
import streamlit as st
import openai
import PyPDF2

st.set_page_config(page_title="SleuthIQ Discovery Assistant", page_icon="🔍")
st.title("🔍 SleuthIQ Discovery Assistant")
st.markdown("#### Powered by Zelaya & Associates")

# Replace with your actual API key
openai.api_key = "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"

ANALYSIS_OPTIONS = {
    "Detailed Analysis": "creates a detailed summary of the document",
    "Investigative Action Plan": "provides a summary and breakdown of investigative suggestions from a defense perspective",
    "Evidence Analysis": "provides summary and recommendation for forensic experts based on likelihood of success",
    "Reasonable Doubt and Beyond Reasonable Doubt Analysis": "provides strengths for defense and prosecution, and a comparative analysis"
}

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    return "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())

def analyze_with_openai(text, analysis_type):
    prompt = f"""You are a board-certified criminal defense investigator.
You will receive a document or discovery file and must perform the following type of analysis: {analysis_type}.
Respond clearly and thoroughly.

Document:
{text[:3000]}...

---

Your Analysis ({analysis_type}):"""
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
analysis_type = st.selectbox("Select Analysis Type", list(ANALYSIS_OPTIONS.keys()))
submit_button = st.button("Run Analysis")

if submit_button and uploaded_file and analysis_type:
    with st.spinner("Processing file and generating analysis..."):
        try:
            text = extract_text_from_pdf(uploaded_file)
            if not text:
                st.error("Could not extract any text from the PDF.")
            else:
                result = analyze_with_openai(text, analysis_type)
                st.success("Analysis complete:")
                st.text_area("Result", result, height=400)
        except Exception as e:
            st.error(f"An error occurred: {e}")
elif submit_button:
    st.warning("Please upload a PDF and select an analysis type.")

st.markdown("---")
st.caption("© 2025 SleuthIQ | Zelaya & Associates")
