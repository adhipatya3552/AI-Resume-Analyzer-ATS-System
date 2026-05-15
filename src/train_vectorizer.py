import pickle

from sklearn.feature_extraction.text import TfidfVectorizer

from src.job_loader import load_jobs


df = load_jobs(
    "data/jobs/job_descriptions.csv"
)

documents = df["Description"].fillna("").tolist()

vectorizer = TfidfVectorizer()

vectorizer.fit(documents)

pickle.dump(
    vectorizer,
    open(
        "models/tfidf_vectorizer.pkl",
        "wb"
    )
)

print("Vectorizer saved successfully.")