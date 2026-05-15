import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st

from src.formatter import format_job_description
from src.pdf_parser import extract_text
from src.preprocess import clean_text
from src.skill_extractor import extract_skills
from src.similarity_engine import calculate_similarity
from src.recommendation_engine import missing_skills
from src.job_loader import load_jobs, get_job_titles, get_job_description
from src.utils import save_uploaded_file


# ----------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

st.title("🤖 AI Resume Analyzer & ATS System")

st.write("Upload your resume and compare it with job descriptions.")

# ----------------------------
# Load Jobs Dataset
# ----------------------------

jobs_df = load_jobs("data/jobs/job_descriptions.csv")

job_titles = get_job_titles(jobs_df)

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.header("Select Job Role")

selected_job = st.sidebar.selectbox("Choose Job Title", job_titles)

job_description = get_job_description(jobs_df, selected_job)

# ----------------------------
# Job Description Preview (always visible)
# ----------------------------

st.subheader("📄 Job Description")

format_job_description(job_description)

st.divider()

# ----------------------------
# Resume Upload
# ----------------------------

uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])

# ----------------------------
# Analyze
# ----------------------------

if st.button("Analyze Resume"):

    if uploaded_resume:

        # Save Resume
        resume_path = save_uploaded_file(uploaded_resume)

        # Extract Text
        resume_text = extract_text(resume_path)

        # Clean Text
        cleaned_resume = clean_text(resume_text)
        cleaned_job = clean_text(job_description)

        # Similarity Score
        similarity_score = calculate_similarity(cleaned_resume, cleaned_job)

        # Extract Skills
        resume_skills = extract_skills(cleaned_resume)
        job_skills = extract_skills(cleaned_job)

        # Missing Skills
        missing = missing_skills(resume_skills, job_skills)

        # ----------------------------
        # Display Results
        # ----------------------------

        st.subheader("📊 ATS Match Score")

        st.progress(int(similarity_score))
        st.success(f"Match Score: {similarity_score}%")

        # ----------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Resume Skills")

            st.write(resume_skills)

        with col2:

            st.subheader("❌ Missing Skills")

            st.write(missing)



    else:

        st.warning(
            "Please upload a resume."
        )