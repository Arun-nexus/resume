import pandas as pd
from sentence_transformers import SentenceTransformer
from logger import logging
from notebook.configuration_file import save_pickle,open_pickle,safe_parse
import os 


def preprocessing(data: pd.DataFrame):
    try:
        logging.info("data preprocessing has been started")

        skills = data["skills"].astype(str).tolist()
        label = data["title"].astype(str).tolist()

        logging.info("data was successfully divided into skills and label")

        if os.path.exists("data/transformer"):
            transformer = SentenceTransformer("data/transformer")
        else:
            transformer = SentenceTransformer("all-MiniLM-L6-v2")
            transformer.save("data/transformer")

        logging.info("sentence transformer has been called successfully")

        embedded_skills = transformer.encode(skills)

        logging.info("skills has been vectorized successfully")

        save_pickle("data/embedded_skills.pkl", embedded_skills)
        save_pickle("data/label.pkl", label)
        
        logging.info("vectors and transformer stored successfully")

    except Exception as e:
        logging.error(f"error occured in data preprocessing file during preprocessing of data as {e}")
        raise

if __name__ == "__main__":
    preprocessing(pd.read_csv(r"data\dataset.csv"))