import dotenv
import os

dotenv.load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("API_KEY")
token = os.getenv("TOKEN")

print(f"API_KEY: {api_key}")
print(f"TOKEN: {token}")

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {
        "item_id": item_id,
        "query": q,
    }
