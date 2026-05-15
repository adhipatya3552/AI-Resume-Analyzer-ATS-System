import pandas as pd


def load_jobs(csv_path):

    df = pd.read_csv(csv_path)

    return df


def get_job_titles(df):

    return df["Job Title"].dropna().unique()


def get_job_description(df, title):

    row = df[df["Job Title"] == title]

    if not row.empty:
        desc = row.iloc[0]["Description"]
        # Fix common merged words/typos from the raw CSV
        desc = desc.replace("businessrelevant", "business relevant")
        desc = desc.replace("bipython", "bi python")
        desc = desc.replace("datadriven", "data driven")
        desc = desc.replace("shortrange", "short range")
        desc = desc.replace("renewalretention", "renewal retention")
        desc = desc.replace("memberfacing", "member facing")
        return desc

    return ""