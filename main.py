from src.pdf_parser import extract_text
from src.preprocess import clean_text
from src.skill_extractor import extract_skills
from src.similarity_engine import calculate_similarity
from src.recommendation_engine import missing_skills
from src.job_loader import load_jobs, get_job_titles, get_job_description


# -----------------------------------
# LOAD RESUME
# -----------------------------------

resume_path = ("data/resumes/engineering_lab_techinician.pdf")

resume_text = extract_text(resume_path)

cleaned_resume = clean_text(resume_text)

resume_skills = extract_skills(cleaned_resume)

# -----------------------------------
# LOAD JOB DATASET
# -----------------------------------

jobs_df = load_jobs("data/jobs/job_descriptions.csv")

job_titles = get_job_titles(jobs_df)

# -----------------------------------
# SELECT JOB ROLE
# -----------------------------------

selected_job = job_titles[0]

job_description = get_job_description(jobs_df,selected_job)

cleaned_job = clean_text(job_description)

job_skills = extract_skills(cleaned_job)

# -----------------------------------
# CALCULATE ATS SCORE
# -----------------------------------

similarity_score = calculate_similarity(cleaned_resume,cleaned_job)

# -----------------------------------
# FIND MISSING SKILLS
# -----------------------------------

missing = missing_skills(resume_skills,job_skills)

# -----------------------------------
# PRINT RESULTS
# -----------------------------------

print("\n========== AI RESUME ANALYZER ==========\n")

print(f"Selected Job Role: {selected_job}")

print(f"\nATS Match Score: {similarity_score}%")

print("\n========== RESUME SKILLS ==========\n")

print(resume_skills)

print("\n========== JOB SKILLS ==========\n")

print(job_skills)

print("\n========== MISSING SKILLS ==========\n")

print(missing)

print("\n=======================================\n")