# 🤖 AI Resume Analyzer & ATS System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-TF--IDF%20%2B%20Cosine-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-Text%20Preprocessing-green?style=for-the-badge)
![pdfplumber](https://img.shields.io/badge/pdfplumber-PDF%20Parser-blueviolet?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-Job%20Dataset-150458?style=for-the-badge&logo=pandas&logoColor=white)

**An AI-powered Resume Analyzer and ATS (Applicant Tracking System) that reads your resume PDF, compares it against real job descriptions, calculates an ATS match score using TF-IDF and cosine similarity, and tells you exactly which skills you are missing — with both a CLI and a Streamlit web interface.**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [How the System Works](#-how-the-system-works)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Dataset](#-dataset)
- [Sample Resumes](#-sample-resumes)
- [Getting Started](#-getting-started)
- [Running the Project](#-running-the-project)
- [Training the TF-IDF Vectorizer](#-training-the-tf-idf-vectorizer)
- [Module Reference](#-module-reference)
- [Known Limitations](#-known-limitations)
- [Roadmap](#-roadmap)

---

## 🧠 Overview

This project is an **AI Resume Analyzer and ATS (Applicant Tracking System)** built entirely in Python. It takes a resume PDF as input, compares it against job descriptions from a CSV dataset, and gives you three things:

- 📊 **ATS Match Score** — a percentage that tells you how closely your resume matches the selected job description, calculated using TF-IDF vectorization and cosine similarity
- ✅ **Resume Skills** — the list of technical skills found in your resume
- ❌ **Missing Skills** — the skills that the job description requires but are not found in your resume

The system works the same way real ATS software does at companies — it compares text similarity between a resume and a job description and scores how well they match.

You can run it either as a **command-line script** using `main.py` for quick testing, or as a fully interactive **Streamlit web app** using `app/app.py` where you can upload any resume PDF and pick from different job roles.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **PDF Resume Parsing** | Extracts raw text from any resume PDF using `pdfplumber` |
| 🧹 **Text Preprocessing** | Lowercases text, removes special characters, strips NLTK stopwords |
| 🔍 **Skill Extraction** | Matches resume and job description text against a curated skills database |
| 📊 **ATS Score Calculation** | Uses TF-IDF + Cosine Similarity to calculate a percentage match score |
| ❌ **Missing Skills Detection** | Compares resume skills vs job skills and highlights what's missing |
| 📋 **Formatted Job Descriptions** | Parses raw job description text into structured sections with headings and bullet points |
| 🖥️ **CLI Interface** | Quick terminal-based testing with printed results |
| 🌐 **Streamlit Web App** | Upload resume, pick job role, view score and skill gaps in a clean browser UI |
| 💾 **TF-IDF Vectorizer Training** | Trains and saves a TF-IDF vectorizer on all job descriptions for potential reuse |

---

## ⚙️ How the System Works

The project is broken into separate modules, each responsible for one step of the pipeline. Here is a complete walkthrough of the entire flow:

### Step 1 — PDF Parsing (`src/pdf_parser.py`)

The first step is to read the resume. The user either provides a PDF file path (in the CLI) or uploads a PDF through the Streamlit app. `pdfplumber` opens the PDF and reads it page by page. For each page, it extracts all the text and appends it together into one long string.

> **In simple words:** It's like copying all the text out of a PDF into a plain text document so the rest of the code can work with it.

---

### Step 2 — Text Preprocessing (`src/preprocess.py`)

Raw text from a PDF is messy — it has punctuation, numbers, symbols, and common words like "the", "is", "and" that carry no useful information. This module cleans all of that up in three steps:

1. Converts everything to **lowercase** so "Python" and "python" are treated the same
2. Removes everything except **alphabetic characters and spaces** using a regex pattern — this strips numbers, punctuation, and special characters
3. Removes **English stopwords** using NLTK's built-in stopwords list (words like "the", "a", "of", "in", etc. that appear everywhere but mean nothing for comparison)

The same cleaning function is applied to both the resume text and the job description text before any comparison is done, so both are normalized consistently.

> **In simple words:** It strips the noise from the text and keeps only the meaningful words so the comparison is accurate.

---

### Step 3 — Skill Extraction (`src/skill_extractor.py`)

This module scans the cleaned text and looks for known technical skills by comparing every word or phrase against a **manually curated skills database** (`skills_db`). The database currently contains 23 in-demand technical skills including:

`python`, `java`, `c++`, `machine learning`, `deep learning`, `tensorflow`, `pytorch`, `sql`, `docker`, `kubernetes`, `fastapi`, `streamlit`, `nlp`, `pandas`, `numpy`, `scikit-learn`, `data analysis`, `data science`, `aws`, `rest api`, `flask`, `git`, `github`

The function checks if each skill from the database appears anywhere in the text (case-insensitive). If it does, it adds it to the found skills list. Duplicates are removed using `set()`.

This function runs **separately on the resume text and the job description text**, so you get two skill lists — one for what the candidate has, and one for what the job requires.

> **In simple words:** It reads through the text and highlights any technical skills it recognises from its known list.

---

### Step 4 — ATS Score Calculation (`src/similarity_engine.py`)

This is the core of the system. It calculates how closely the resume matches the job description using two standard NLP techniques:

**TF-IDF (Term Frequency-Inverse Document Frequency):**
Both the cleaned resume text and cleaned job description text are passed to `TfidfVectorizer` from scikit-learn. TF-IDF converts each text into a numerical vector. Words that appear often in one document but rarely across all documents get higher weights — meaning rare but important words carry more significance than common ones.

**Cosine Similarity:**
Once both texts are converted into TF-IDF vectors, `cosine_similarity` measures the angle between the two vectors. A cosine similarity of 1.0 means the texts are identical. A score of 0.0 means they share nothing in common.

The cosine similarity value (between 0 and 1) is multiplied by 100 and rounded to two decimal places to give the final **ATS Match Score as a percentage**.

> **In simple words:** It measures how much the vocabulary and content of your resume overlaps with the vocabulary and content of the job description, and turns that overlap into a percentage score.

---

### Step 5 — Missing Skills Detection (`src/recommendation_engine.py`)

This is the simplest but most actionable part. It takes the two skill lists — one from the resume, one from the job description — and loops through the job skills. Any skill that appears in the job description but is NOT found in the resume is added to a `missing` list.

This list is what tells the candidate exactly which skills they need to add to their resume to improve their chances.

> **In simple words:** It subtracts what you have from what the job needs and shows you the gap.

---

### Step 6 — Job Description Formatting (`src/formatter.py`)

Raw job descriptions in the CSV are long unformatted text strings — everything is squished together with no headings or bullet points. The `formatter.py` module intelligently parses these strings and renders them as clean, structured HTML inside the Streamlit app.

It works in three stages:
1. Scans the raw text for known **section keywords** like "Key Responsibilities", "Requirements", "Qualifications", "Benefits", "About Us", "What You Will Do", etc. using a pre-compiled regex pattern
2. Splits the text at each detected section heading to isolate the content of each section
3. Further splits each section's content into **individual bullet points** (splitting on full stops) and renders them as an HTML unordered list with a blue `▸` bullet marker

If no recognizable sections are found, the text is rendered as a simple readable paragraph. All styling is injected via custom CSS directly into Streamlit using `st.markdown(..., unsafe_allow_html=True)`.

> **In simple words:** It takes a wall of plain text and turns it into a nicely formatted job description with headings and bullet points, the way you'd normally see it on a job board.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                       USER INPUT                              │
│          Resume PDF (upload) + Job Role (dropdown)            │
└──────────────────────────────┬───────────────────────────────┘
                               │
                  ┌────────────▼────────────┐
                  │      app/app.py          │
                  │  (Streamlit Web UI)      │
                  └──┬──────────────────┬───┘
                     │                  │
        ┌────────────▼──┐        ┌──────▼──────────────┐
        │  Resume PDF   │        │   Job Description    │
        │  Processing   │        │   from CSV Dataset   │
        └────────────┬──┘        └──────┬───────────────┘
                     │                  │
        ┌────────────▼──────┐    ┌──────▼───────────────┐
        │   pdf_parser.py   │    │    job_loader.py      │
        │ (Extract raw text)│    │ (Load CSV, get title  │
        └────────────┬──────┘    │  and description)     │
                     │           └──────┬───────────────┘
        ┌────────────▼──────┐           │
        │   preprocess.py   │◄──────────┘
        │ (Clean both texts)│
        └──┬─────────────┬──┘
           │             │
  ┌────────▼──────┐  ┌───▼──────────────────┐
  │skill_extractor│  │  similarity_engine.py │
  │.py            │  │  (TF-IDF + Cosine     │
  │(Find skills   │  │   Similarity → Score) │
  │ in resume and │  └───────────────────────┘
  │ in job desc)  │
  └────────┬──────┘
           │
  ┌────────▼──────────────┐
  │ recommendation_engine │
  │ .py                   │
  │ (Job skills minus     │
  │  Resume skills =      │
  │  Missing skills)      │
  └────────┬──────────────┘
           │
  ┌────────▼──────────────┐
  │      app/app.py        │
  │  Display:              │
  │  - ATS Score Bar       │
  │  - Resume Skills       │
  │  - Missing Skills      │
  └───────────────────────┘
```

**Full Data Flow:**

```
Resume PDF
     │
     ▼
pdf_parser.py  ──▶  Raw text string
     │
     ▼
preprocess.py  ──▶  Cleaned, normalized text
     │
     ├──────────────────────────────────────────┐
     ▼                                          ▼
skill_extractor.py                    similarity_engine.py
(Skills found in resume)              (TF-IDF vectorize both
     │                                 cleaned texts → cosine
     │                                 similarity → ATS Score %)
     │                                          │
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Job Description CSV
     │
     ▼
job_loader.py  ──▶  Selected job description text
     │
     ▼
preprocess.py  ──▶  Cleaned job text
     │
     ▼
skill_extractor.py  ──▶  Skills found in job description
     │
     ▼
recommendation_engine.py  ──▶  Missing skills (job skills - resume skills)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All results ──▶  app/app.py  ──▶  Displayed in Streamlit UI
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.10+ | Core programming language |
| **Web UI** | Streamlit | Browser-based interactive interface |
| **PDF Parsing** | pdfplumber | Extracting text from resume PDF files |
| **Text Preprocessing** | NLTK | Stopword removal and text normalization |
| **Vectorization** | Scikit-Learn `TfidfVectorizer` | Converting text into TF-IDF numerical vectors |
| **Similarity Scoring** | Scikit-Learn `cosine_similarity` | Calculating the ATS match percentage |
| **Job Dataset** | Pandas | Loading and querying the job descriptions CSV |
| **Skill Matching** | Custom keyword database | Matching skills against a curated list of 23 tech skills |
| **HTML Formatting** | Custom regex + Streamlit `st.markdown` | Parsing and rendering structured job descriptions |
| **Model Saving** | Pickle | Saving the trained TF-IDF vectorizer to disk |
| **Visualization** | Streamlit `st.progress` | Displaying the ATS score as a visual progress bar |

---

## 📁 Project Structure

```
ai-resume-analyzer/
│
├── app/
│   └── app.py                      # Main Streamlit web application (UI, layout, analysis flow)
│
├── data/
│   ├── jobs/
│   │   └── job_descriptions.csv    # Dataset of job titles and their descriptions
│   └── resumes/
│       ├── engineering_intern.pdf              # Sample resume 1 for testing
│       ├── engineering_lab_technician.pdf      # Sample resume 2 for testing
│       └── software_engineering_manager.pdf    # Sample resume 3 for testing
│
├── models/
│   └── tfidf_vectorizer.pkl        # Saved TF-IDF vectorizer (generated by train_vectorizer.py)
│
├── notebooks/
│   └── experimentation.ipynb       # Jupyter notebook used for testing individual components
│
├── src/
│   ├── formatter.py                # Parses raw job description text into structured HTML sections
│   ├── job_loader.py               # Loads job_descriptions.csv and retrieves titles/descriptions
│   ├── pdf_parser.py               # Extracts text from PDF files using pdfplumber
│   ├── preprocess.py               # Cleans text (lowercase, remove symbols, remove stopwords)
│   ├── recommendation_engine.py    # Finds missing skills by comparing resume vs job skill lists
│   ├── similarity_engine.py        # TF-IDF + cosine similarity → ATS match score
│   ├── skill_extractor.py          # Matches text against skills_db to find present skills
│   ├── train_vectorizer.py         # Trains TF-IDF on all job descriptions and saves it as pkl
│   └── utils.py                    # Saves uploaded PDF to the uploads/ folder
│
├── uploads/                        # Temp folder where uploaded resumes are saved (auto-created)
│
├── main.py                         # CLI script for quick terminal-based analysis
└── requirements.txt                # Python dependencies
```

---

## 📊 Dataset

### Source

The job descriptions dataset used in this project was taken from Kaggle, published by **Jayakishan225**:

> 🔗 **Kaggle Link:** [https://www.kaggle.com/datasets/jayakishan225/job-descriptions-dataset](https://www.kaggle.com/datasets/jayakishan225/job-descriptions-dataset)

Download the CSV file from the above link and place it at `data/jobs/job_descriptions.csv` before running the project.

### Column Structure

The dataset is stored at `data/jobs/job_descriptions.csv` and contains two columns:

| Column | Description |
|--------|-------------|
| `Job Title` | The title of the job role (e.g., `Data Analyst`, `Software Engineer`) |
| `Description` | The full raw job description text including responsibilities, requirements, and qualifications |

The `job_loader.py` module also applies a few text fixes to clean up common merged words found in the raw CSV data, such as:

| Raw (broken) | Fixed |
|-------------|-------|
| `businessrelevant` | `business relevant` |
| `bipython` | `bi python` |
| `datadriven` | `data driven` |
| `shortrange` | `short range` |
| `renewalretention` | `renewal retention` |
| `memberfacing` | `member facing` |

These were likely caused by formatting issues in the original data source.

---

## 📄 Sample Resumes

### Source

The sample resume PDF files included in this project were taken from a resume dataset available on Kaggle, published by **Sneha Anbhawal**:

> 🔗 **Kaggle Link:** [https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset)

Three resumes from this dataset are included in `data/resumes/` so you can test the system right away without needing your own resume:

| File | Role |
|------|------|
| `engineering_intern.pdf` | Entry-level engineering intern profile |
| `engineering_lab_technician.pdf` | Lab technician with technical skills |
| `software_engineering_manager.pdf` | Senior software engineering manager profile |

These resumes cover a range of experience levels and skill sets, making them useful for testing the ATS score and missing skills detection across different job roles.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or above
- pip

---

### 1. Clone the Repository

```bash
git clone https://github.com/adhipatya3552/AI-Resume-Analyzer-ATS-System.git
cd AI-Resume-Analyzer-ATS-System
```

---

### 2. Create a Virtual Environment

It is recommended to create a virtual environment first so all libraries get installed in an isolated space and don't affect your system Python.

```bash
# Create virtual environment
python -m venv venv

# Activate — on Windows
venv\Scripts\activate

# Activate — on Mac/Linux
source venv/bin/activate
```

---

### 3. Install Dependencies

Once the virtual environment is active:

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
```
streamlit
pandas
numpy
scikit-learn
nltk
pdfplumber
matplotlib
plotly
```

---

### 4. Download NLTK Stopwords

The preprocessing module uses NLTK's English stopwords. On the first run, NLTK will try to download this automatically, but if it doesn't, you can run this once manually:

```python
import nltk
nltk.download("stopwords")
```

Or just run the app — the `preprocess.py` module calls `nltk.download("stopwords")` at import time, so it downloads automatically.

---

## ▶️ Running the Project

### Option 1 — Streamlit Web App (Recommended)

```bash
streamlit run app/app.py
```

The app opens in your browser at `http://localhost:8501`.

**How to use it:**

1. On the **left sidebar**, use the **"Choose Job Title"** dropdown to select a job role from the dataset
2. The **Job Description** section on the main page shows the formatted description for the selected role — with section headings and bullet points
3. Click **"Upload Resume PDF"** and select your resume file
4. Click the **"Analyze Resume"** button
5. The app will display:
   - 📊 **ATS Match Score** — shown as a progress bar and a percentage
   - ✅ **Resume Skills** — all skills found in your resume
   - ❌ **Missing Skills** — skills the job needs that are not in your resume

---

### Option 2 — CLI (Terminal)

For quick testing without the web UI:

```bash
python main.py
```

By default, `main.py` loads the resume at `data/resumes/engineering_lab_technician.pdf` and compares it against the first job title in the dataset.

**Sample output:**

```
========== AI RESUME ANALYZER ==========

Selected Job Role: Data Analyst

ATS Match Score: 34.27%

========== RESUME SKILLS ==========
['python', 'sql', 'data analysis', 'pandas']

========== JOB SKILLS ==========
['python', 'sql', 'data analysis', 'pandas', 'numpy', 'aws', 'machine learning']

========== MISSING SKILLS ==========
['numpy', 'aws', 'machine learning']

=======================================
```

To test with a different resume or job, edit these lines in `main.py`:

```python
resume_path = "data/resumes/your_resume.pdf"   # Change resume path
selected_job = job_titles[0]                    # Change index for different job
```

---

## 🧠 Training the TF-IDF Vectorizer

The `src/train_vectorizer.py` script trains a TF-IDF vectorizer on all the job descriptions in the dataset and saves it as a pickle file. This allows the vectorizer to be reused later without retraining.

```bash
python src/train_vectorizer.py
```

This will:
1. Load all job descriptions from `data/jobs/job_descriptions.csv`
2. Fit a `TfidfVectorizer` on the full `Description` column
3. Save the trained vectorizer to `models/tfidf_vectorizer.pkl`

> Note: The current `similarity_engine.py` fits a fresh vectorizer on each comparison (resume + one job description). The saved pkl vectorizer in `models/` is intended for future use — for example, to rank all jobs against a resume simultaneously without refitting each time.

---

## 📦 Module Reference

### `src/pdf_parser.py`

Opens a PDF file using `pdfplumber` and reads it page by page. Concatenates the extracted text from all pages into a single string.

```python
text = extract_text("data/resumes/my_resume.pdf")
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `pdf_path` | `str` | Path to the PDF file to read |

**Returns:** A single string with all extracted text from the PDF.

---

### `src/preprocess.py`

Cleans raw text by converting to lowercase, removing non-alphabetic characters using regex, and filtering out English stopwords using NLTK.

```python
cleaned = clean_text(raw_text)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Raw text to clean |

**Returns:** A cleaned, normalized string with only meaningful words remaining.

---

### `src/skill_extractor.py`

Scans the given text and checks it against the built-in `skills_db` list. Returns all skills found in the text.

```python
skills = extract_skills(cleaned_text)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Cleaned text to scan for skills |

**Returns:** A deduplicated list of skill strings found in the text.

**Current skills database (23 skills):**
`python`, `java`, `c++`, `machine learning`, `deep learning`, `tensorflow`, `pytorch`, `sql`, `docker`, `kubernetes`, `fastapi`, `streamlit`, `nlp`, `pandas`, `numpy`, `scikit-learn`, `data analysis`, `data science`, `aws`, `rest api`, `flask`, `git`, `github`

---

### `src/similarity_engine.py`

Converts both the resume text and job description text into TF-IDF vectors and calculates their cosine similarity as a percentage.

```python
score = calculate_similarity(cleaned_resume, cleaned_job)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `resume_text` | `str` | Cleaned resume text |
| `job_text` | `str` | Cleaned job description text |

**Returns:** A `float` — the ATS match score as a percentage (e.g., `67.43`).

---

### `src/job_loader.py`

Loads the job descriptions CSV and provides functions to get job titles and retrieve the description for a selected title.

```python
jobs_df = load_jobs("data/jobs/job_descriptions.csv")
titles  = get_job_titles(jobs_df)
desc    = get_job_description(jobs_df, "Data Analyst")
```

| Function | Parameters | Returns |
|----------|-----------|---------|
| `load_jobs(csv_path)` | Path to CSV | Full DataFrame |
| `get_job_titles(df)` | DataFrame | Array of unique job title strings |
| `get_job_description(df, title)` | DataFrame + title string | Job description string (with text fixes applied) |

---

### `src/recommendation_engine.py`

Compares resume skills against job skills and returns any skills that appear in the job but not in the resume.

```python
missing = missing_skills(resume_skills, job_skills)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `resume_skills` | `list` | Skills found in the resume |
| `job_skills` | `list` | Skills found in the job description |

**Returns:** A list of skill strings that are missing from the resume.

---

### `src/formatter.py`

Parses a raw, unformatted job description string and renders it as structured HTML inside Streamlit. Detects section headings like "Key Responsibilities", "Requirements", "Qualifications", "Benefits", etc. and renders each section with a styled heading and bullet points.

```python
format_job_description(job_description_text)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Raw job description string from the CSV |

**Returns:** Nothing — directly renders HTML into the active Streamlit page using `st.markdown`.

Supported section keywords: `key responsibilities`, `responsibilities`, `preferred qualifications`, `qualifications`, `requirements`, `nice to have`, `bonus`, `benefits`, `about us`, `about the role`, `job overview`, `overview`, `what you will do`, `what we offer`

---

### `src/utils.py`

Saves a Streamlit `UploadedFile` object to the `uploads/` folder on disk so it can be read as a regular file by `pdfplumber`.

```python
file_path = save_uploaded_file(uploaded_file)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `uploaded_file` | Streamlit `UploadedFile` | The file object from `st.file_uploader` |
| `upload_folder` | `str` | Folder to save to (default: `"uploads"`) |

**Returns:** The full file path as a string.

---

## ⚠️ Known Limitations

| Issue | Details |
|-------|---------|
| **Small skills database** | The `skills_db` list has only 23 skills. Many real-world skills like React, Node.js, Excel, Tableau, Figma, etc. are not covered. Skills not in the list will never be detected. |
| **Keyword-based skill matching** | Skill extraction uses simple substring matching. It won't detect variations — for example, "ML" won't match "machine learning", and "Py" won't match "python". |
| **ATS score can be low for good resumes** | TF-IDF compares vocabulary overlap. If a resume uses different but equivalent words (e.g., "developed" vs "built"), the score may be lower than expected even if the experience is a match. |
| **Scanned or image-based PDFs** | `pdfplumber` can only extract selectable text. If a resume is a scanned image, no text will be extracted and the app will produce empty results. |
| **Hardcoded resume in CLI** | `main.py` has the resume path hardcoded. To test a different resume you need to manually edit the file. |
| **No user accounts or history** | The app doesn't store results. Every analysis is a fresh run — nothing is saved between sessions. |
| **Single job comparison at a time** | The app compares your resume against one job at a time. There is no bulk scoring against all jobs simultaneously. |
| **Job descriptions only** | The system only reads from the local CSV file. It cannot pull live job listings from LinkedIn, Naukri, or any job board. |

---

## 🗺️ Roadmap

- [x] PDF text extraction using pdfplumber
- [x] Text preprocessing (lowercase, regex cleaning, stopword removal)
- [x] Keyword-based skill extraction with a curated skills_db
- [x] ATS score calculation using TF-IDF + cosine similarity
- [x] Missing skills detection and display
- [x] Job descriptions CSV loader with text fix handling
- [x] Structured job description formatter (section detection + bullet points)
- [x] Streamlit web app (sidebar job selector, PDF upload, score bar, skills columns)
- [x] CLI interface for quick testing
- [x] TF-IDF vectorizer training and saving with pickle
- [x] Sample resumes included for testing
- [ ] Expand skills database to 100+ skills across more domains
- [ ] Add fuzzy/semantic matching for skill synonyms (e.g., "ML" = "machine learning")
- [ ] Score resume against all jobs in the dataset at once and rank by best match
- [ ] Generate a downloadable PDF report of the analysis results
- [ ] Add resume improvement suggestions beyond just skill gaps
- [ ] Support DOCX resume files in addition to PDF
- [ ] Add charts showing skill overlap visually using Plotly
- [ ] Deploy the Streamlit app on Streamlit Cloud

---

<div align="center">

Built with ❤️ using Python, Scikit-Learn, NLTK, pdfplumber, and Streamlit.

</div>
