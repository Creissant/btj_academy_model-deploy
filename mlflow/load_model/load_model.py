import os
from dotenv import load_dotenv
import pandas as pd
import mlflow
import mlflow.sklearn

# Load environment variables
load_dotenv(".env.development")

# MLflow tracking
mlflow.set_tracking_uri(f"http://{os.getenv('MLFLOW_TRACKING_URI_IP')}:{os.getenv('MLFLOW_TRACKING_URI_PORT')}")

# Load the model from the Model Registry
MODEL_NAME = "TitanicMLPModel"
MODEL_VERSION = "latest"
MODEL_URI = f"models:/{MODEL_NAME}/{MODEL_VERSION}"

model = mlflow.sklearn.load_model(MODEL_URI)

# Contoh data baru (formatnya harus sama dengan input training pipeline)
X_new = pd.DataFrame([{
    "Pclass": 3,
    "Sex": "male",
    "Age": 22,
    "SibSp": 1,
    "Parch": 0,
    "Fare": 7.25,
    "Embarked": "S",
    "NameTitle": "Mr"
}])

# Predition
y_pred = model.predict(X_new)
y_pred_proba = model.predict_proba(X_new)

print("Prediction:", y_pred)
print("Probabilities:", y_pred_proba)