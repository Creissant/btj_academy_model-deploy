from pathlib import Path
import joblib
import pandas as pd

from fastapi import HTTPException

from api.predict.schema import TitanicParams

# Load model langsung
# MODEL_PATH = "models\titanic_model.pkl"
# model = joblib.load(MODEL_PATH)

# Load model + handling cross platform
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "models" / "titanic_model.pkl"
model = joblib.load(MODEL_PATH)

class PredictTitanic:
    def __init__(self, params: TitanicParams):
        self.params = params

    def predict(self):
        try:
            df = pd.DataFrame([self.params.model_dump()])

            # Prediksi kelas
            prediction = model.predict(df)[0]
            
            # Prediksi probabilitas (confidence)
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(df)[0].tolist()
            else:
                proba = None

            return {
                "result": int(prediction),
                "probability": proba,
                "message": "Prediction success"
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
