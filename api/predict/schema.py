from pydantic import BaseModel
from typing import List, Optional

class TitanicParams(BaseModel):
    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str
    NameTitle: str

class PredictionResult(BaseModel):
    message: str
    result: int
    probability: Optional[List[float]] = None