import yaml
from logger import logging
import pandas as pd
import os
import pickle
import json
import pytesseract
from PIL import Image
import shutil
import io
from pdf2image import convert_from_bytes


import pytesseract
import shutil
import os
from logger import logging

def get_poppler_path():
    try:
        env_path = os.getenv("POPPLER_PATH")
        if env_path and os.path.exists(env_path):
            logging.info(f"Poppler from ENV: {env_path}")
            return env_path

        system_path = shutil.which("pdftoppm")
        if system_path:
            poppler_bin = os.path.dirname(system_path)
            logging.info(f"Poppler found in system PATH: {poppler_bin}")
            return poppler_bin

        windows_path = r"C:\Users\Arun\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"
        if os.path.exists(windows_path):
            logging.info(f"Poppler using Windows fallback: {windows_path}")
            return windows_path

        logging.warning("Poppler not found, using default behavior")
        return None

    except Exception as e:
        logging.error(f"Poppler detection failed: {e}")
        return None

def setup_tesseract():
    try:
        env_path = os.getenv("TESSERACT_CMD")

        if env_path and os.path.exists(env_path):
            pytesseract.pytesseract.tesseract_cmd = env_path
            logging.info(f"Tesseract set from ENV: {env_path}")
            return

        system_path = shutil.which("tesseract")

        if system_path:
            pytesseract.pytesseract.tesseract_cmd = system_path
            logging.info(f"Tesseract found in system PATH: {system_path}")
            return

        windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        if os.path.exists(windows_path):
            pytesseract.pytesseract.tesseract_cmd = windows_path
            logging.info(f"Tesseract using Windows fallback: {windows_path}")
            return

        raise Exception("Tesseract not found anywhere")

    except Exception as e:
        logging.error(f"Tesseract setup failed: {e}")
        raise


def load_parameters() -> dict:
    try:
        with open("params.yaml", "r") as file:
            params = yaml.safe_load(file)
        logging.debug("Parameters loaded successfully")
        return params
    except FileNotFoundError as e:
        logging.error(f"params.yaml not found: {e}")
        raise


def load_data(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path)
        logging.info("Data loaded successfully")
        return df
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise


def save_data(path: str, file):
    try:
        data = pd.DataFrame(file)
        data.to_csv(path, index=False)
    except Exception as e:
        logging.error(f"Error saving data: {e}")
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


def extract_text_from_image_bytes(file_bytes: bytes) -> str:
    try:
        img = Image.open(io.BytesIO(file_bytes))
        img = img.convert("L")

        text = pytesseract.image_to_string(img)

        if not text.strip():
            raise ValueError("No text extracted from image")

        return text

    except Exception as e:
        logging.error(f"OCR (image) failed: {e}")
        raise


def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    try:
        poppler_path = get_poppler_path()
        images = convert_from_bytes(file_bytes,poppler_path=poppler_path)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img)

        if not text.strip():
            raise ValueError("No text extracted from PDF")

        return text

    except Exception as e:
        logging.error(f"OCR (PDF) failed: {e}")
        raise


def extract_text(file_bytes: bytes, filename: str) -> str:
    try:

        if len(file_bytes) > 5 * 1024 * 1024:
            raise ValueError("File too large. Max 5MB allowed.")

        filename = filename.lower()

        if filename.endswith(".pdf"):
            return extract_text_from_pdf_bytes(file_bytes)

        elif filename.endswith((".png", ".jpg", ".jpeg")):
            return extract_text_from_image_bytes(file_bytes)

        else:
            raise ValueError("Unsupported file type")

    except Exception as e:
        logging.error(f"Text extraction failed: {e}")
        raise


def safe_parse(output: str):
    try:
        return json.loads(output)

    except json.JSONDecodeError:
        start = output.find("{")
        end = output.rfind("}") + 1

        if start != -1 and end != -1:
            try:
                return json.loads(output[start:end])
            except:
                pass

        raise ValueError("No valid JSON found in response")