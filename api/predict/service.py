from pathlib import Path
import joblib
import pandas as pd
import mlflow
import mlflow.sklearn
import os

from dotenv import load_dotenv

from fastapi import HTTPException

from api.predict.schema import TitanicParams

# Load model langsung
# MODEL_PATH = "models\titanic_model.pkl"
# model = joblib.load(MODEL_PATH)

# Load model + handling cross platform
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "models" / "titanic_model.pkl"

try:
    local_model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    raise FileNotFoundError("Model file not found at path: {MODEL_PATH}")

class PredictTitanic:
    def __init__(self, params: TitanicParams):
        self.params = params

    def predict(self):
        """Prediksi menggunakan model lokal"""
        try:
            df = pd.DataFrame([self.params.model_dump()])

            # Prediksi kelas
            prediction = local_model.predict(df)[0]
            
            # Prediksi probabilitas (confidence)
            if hasattr(local_model, "predict_proba"):
                proba = local_model.predict_proba(df)[0].tolist()
            else:
                proba = None

            return {
                "result": int(prediction),
                "probability": proba,
                "message": "Prediction success"
            }

        except Exception as err:
            raise RuntimeError(f"Prediction failed: {err}") from err

    def predict_v2(self):
        """Prediksi menggunakan model dari MLflow Model Registry"""
        try:
            # Load environment variables
            load_dotenv(".env.development")

            # Setup MLflow tracking server
            mlflow.set_tracking_uri(f"http://{os.getenv('MLFLOW_TRACKING_URI_IP')}:{os.getenv('MLFLOW_TRACKING_URI_PORT')}")

            # Nama model sesuai di MLflow
            model_name = "TitanicMLPModel"
            model_version = "latest"
            model_uri = f"models:/{model_name}/{model_version}"

            # Load model dari registry
            mlflow_model = mlflow.sklearn.load_model(model_uri)

            df = pd.DataFrame([self.params.model_dump()])

            # Prediksi
            prediction = mlflow_model.predict(df)[0]

            if hasattr(mlflow_model, "predict_proba"):
                proba = mlflow_model.predict_proba(df)[0].tolist()
            else:
                proba = None

            return {
                "result": int(prediction),
                "probability": proba,
                "message": "Prediction success (MLflow model)"
            }

        except Exception as err:
            raise RuntimeError(f"Prediction via MLflow failed: {err}") from err