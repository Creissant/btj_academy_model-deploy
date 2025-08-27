from fastapi import APIRouter, HTTPException

from api.predict.schema import TitanicParams, PredictionResult
from api.predict.service import PredictTitanic

# Router + error handling
router = APIRouter(prefix="/predict", tags=["Prediction"])

@router.post("/titanic/v1", response_model=PredictionResult)
def predict_titanic(params: TitanicParams):
    """
    API endpoint untuk memprediksi survival Titanic.
    Input: TitanicParams (Pclass, Age, SibSp, Parch, Fare, Sex, Embarked)
    Output: PredictionResult (hasil prediksi + probabilitas + pesan)
    """
    try:
        prediction_service = PredictTitanic(params)
        pred = prediction_service.predict()

        return PredictionResult(
            message=pred.get("message", ""),
            result=pred.get("result"),
            probability=pred.get("probability")
        )

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error occurred.") from e
    

@router.post("/titanic/v2", response_model=PredictionResult)
def predict_titanic(params: TitanicParams):
    """
    API endpoint untuk memprediksi survival Titanic.
    Input: TitanicParams (Pclass, Age, SibSp, Parch, Fare, Sex, Embarked)
    Output: PredictionResult (hasil prediksi + probabilitas + pesan)
    """
    try:
        prediction_service = PredictTitanic(params)
        pred = prediction_service.predict_v2()

        return PredictionResult(
            message=pred.get("message", ""),
            result=pred.get("result"),
            probability=pred.get("probability")
        )

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Unexpected error occurred.") from e