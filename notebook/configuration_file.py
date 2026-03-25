import yaml
from logger import logging
import pandas as pd
import os
import pickle 
import json
import pytesseract
from PIL import Image
import shutil

def load_parameters() -> dict:
    try:
        with open("params.yaml", 'r') as file:
            params = yaml.safe_load(file)
        logging.debug(f"parameters retrieved from source params.yaml")
        return params
    except FileNotFoundError as e:
        logging.error(f"file not found on params.yaml {e}")
        raise

def load_data(path:str)->pd.DataFrame:
    try:
        df = pd.read_csv(path)
        logging.info("data was successfully loaded. ")
        return df
    except Exception as e:
        logging.error(f"problem occured in data loading for preprocessing as {e}")
        raise

def save_data(path:str,file):
    try:
        
        data = pd.DataFrame(file)
        data.to_csv(path,index = False)
    except Exception as e:
        logging.error(f"file cannot be saved on your given path {e}")
        raise


def save_pickle(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)

def open_pickle(path: str):
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found")
    
    with open(path, "rb") as f:
        return pickle.load(f)



def extract_text_from_image(path):
    try:
        # Check if tesseract is available in system PATH (Docker case)
        tesseract_path = shutil.which("tesseract")

        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            logging.info(f"Tesseract found at: {tesseract_path}")
        else:
            local_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            pytesseract.pytesseract.tesseract_cmd = local_path
            logging.warning(f"Using local tesseract path: {local_path}")

        img = Image.open(path)
        img = img.convert("L")

        text = pytesseract.image_to_string(img)

        if not text.strip():
            raise ValueError("No text extracted from image")

        return text

    except Exception as e:
        logging.error(f"OCR failed: {e}")
        raise

def safe_parse(output):
    try:
        return json.loads(output)
    except:
        start = output.find("{")
        end = output.rfind("}") + 1
        
        if start != -1 and end != -1:
            return json.loads(output[start:end])
        
        raise ValueError("No valid JSON found")