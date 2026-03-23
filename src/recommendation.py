from sentence_transformers.util import cos_sim
from sentence_transformers import SentenceTransformer
from logger import logging
from notebook.configuration_file import open_pickle
import numpy as np

def predicting(new_skills):
    try:
        logging.info("recommendation model has been started")
        recommendation = []
        
        logging.info("loading necessary pickle files")
        skills = open_pickle("data/embedded_skills.pkl")
        labels = open_pickle("data/label.pkl")

        transformer = SentenceTransformer("all-MiniLM-L6-v2")

        logging.info("vectorizing the candidate skills")
        new_emb = transformer.encode([new_skills], batch_size=32, show_progress_bar=True)

        sims = cos_sim(new_emb, skills).cpu().numpy()
    
        logging.info("sorting top skills according to candidate")
        top_k_idx = np.argsort(sims[0])[-3:][::-1]

        seen = set()

        for i in top_k_idx:
            label = labels[i]
            if label not in seen:
                recommendation.append((label, round(float(sims[0][i]), 4)))
                seen.add(label)
        logging.info(f"model suggests: {recommendation}")
        return recommendation

    except Exception as e:
        logging.error(f"error occured: {e}")
        raise


if __name__ == "__main__":
    print(predicting("Python, Machine Learning, Deep Learning, NLP, TensorFlow"))