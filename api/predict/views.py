from fastapi import APIRouter

from api.predict.schema import TitanicParams, PredictionResult
from api.predict.service import PredictTitanic

# Router
router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("/", response_model=PredictionResult)
def predict_titanic(params: TitanicParams):
    """
    API endpoint untuk memprediksi survival Titanic.
    Input: TitanicParams (Pclass, Age, SibSp, Parch, Fare, Sex, Embarked)
    Output: PredictionResult (hasil prediksi + probabilitas + pesan)
    """
    prediction_service = PredictTitanic(params)
    pred = prediction_service.predict()

    return PredictionResult(
        message=pred.get("message", ""),
        result=pred.get("result"),
        probability=pred.get("probability")
    )
