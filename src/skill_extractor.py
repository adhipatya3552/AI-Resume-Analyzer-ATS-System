skills_db = [

    "python",
    "java",
    "c++",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "sql",
    "docker",
    "kubernetes",
    "fastapi",
    "streamlit",
    "nlp",
    "pandas",
    "numpy",
    "scikit-learn",
    "data analysis",
    "data science",
    "aws",
    "rest api",
    "flask",
    "git",
    "github"

]


def extract_skills(text):

    found_skills = []

    for skill in skills_db:

        if skill.lower() in text.lower():

            found_skills.append(skill)

    return list(set(found_skills))