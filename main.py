import os

from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel

from api.predict.views import router as predict_router

# load env file
load_dotenv(".env.development")

# fastapi init
# app = FastAPI()
app = FastAPI(
    title="FastAPI Deployment Practice - Titanic Survival Prediction API",
    description="Dummy project untuk belajar FastAPI + deployment - API untuk memprediksi penumpang Titanic selamat atau tidak",
    version="1.0.0"
)

# Include router
app.include_router(predict_router)


#==================================

# pydantic model
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

# routes
@app.get("/")
async def root():
    return {"message": "Welcome to Titanic Prediction API"}

@app.get("/env")
def read_env():
    return {
        "message": f"Hello, this is {os.getenv('ENV')} environment",
        "debug_mode": os.getenv("DEBUG"),
        "port": os.getenv("DB_PORT"),
        "database": os.getenv("DATABASE_URL") # bukan basepractice - hanya di dev
    }

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

@app.post("/items/")
async def create_item(item: Item):
    return {
        "message": "Item created successfully",
        "item": item
    }