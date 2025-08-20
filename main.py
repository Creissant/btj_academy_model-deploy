import os

from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel

# load env file
load_dotenv(".env.development")

# fastapi init
# app = FastAPI()
app = FastAPI(
    title="FastAPI Deployment Practice",
    description="Dummy project untuk belajar FastAPI + deployment",
    version="0.1.0"
)

# pydantic model
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

# routes
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
def read_test():
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