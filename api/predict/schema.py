from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# Tanpa error handling
# class TitanicParams(BaseModel):
#     Pclass: int
#     Sex: str
#     Age: float
#     SibSp: int
#     Parch: int
#     Fare: float
#     Embarked: str
#     NameTitle: str

# Error handling + constraint in schema
class TitanicParams(BaseModel):
    Pclass: int = Field(ge=1, le=3, example=3, description="Passenger class: 1, 2, or 3")
    Sex: Literal["male", "female"] = Field(example="male", description="Gender of the passenger") # str
    Age: float = Field(ge=0, le=120, example=22,description="Age in years")
    SibSp: int = Field(ge=0, example=1, description="Number of siblings/spouses aboard")
    Parch: int = Field(ge=0, example=0, description="Number of parents/children aboard")
    Fare: float = Field(ge=0, example=7.25, description="Ticket fare")
    Embarked: Literal["C", "Q", "S"] = Field(example="S", description="Port of Embarktion") # str
    NameTitle: Literal["Mr", "Mrs", "Miss", "Master", "Rare"] = Field(example="Mr", description="Passenger's name title")  # str

class PredictionResult(BaseModel):
    message: str
    result: int
    probability: Optional[List[float]] = None