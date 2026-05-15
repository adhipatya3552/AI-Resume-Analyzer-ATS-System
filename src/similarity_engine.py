from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_text):

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([
        resume_text,
        job_text
    ])

    similarity = cosine_similarity(
        vectors[0],
        vectors[1]
    )

    score = similarity[0][0] * 100

    return round(score, 2)