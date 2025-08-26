import requests
import os

from dotenv import load_dotenv

# load env
load_dotenv(".env.development")

# get env value
URL= os.getenv("BE_API_HOST")
PORT= os.getenv("BE_API_PORT")
API_URL = f"http://{URL}:{PORT}/predict/"

def predict_survival(payload: dict):
    """
    Kirim payload ke FastAPI backend dan return hasil prediksi.
    """
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
