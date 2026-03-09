import dotenv
import os

dotenv.load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("API_KEY")
token = os.getenv("TOKEN")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# In-memory products store
_products: dict[int, dict] = {}
_next_id: int = 1


class Product(BaseModel):
    name: str
    description: str | None = None
    price: float


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


# --- Products CRUD ---

@app.get("/products")
def list_products():
    return list(_products.values())


@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in _products:
        raise HTTPException(status_code=404, detail="Product not found")
    return _products[product_id]


@app.post("/products", status_code=201)
def create_product(product: Product):
    global _next_id
    new_product = {"id": _next_id, **product.model_dump()}
    _products[_next_id] = new_product
    _next_id += 1
    return new_product


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    if product_id not in _products:
        raise HTTPException(status_code=404, detail="Product not found")
    updated = {"id": product_id, **product.model_dump()}
    _products[product_id] = updated
    return updated


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    if product_id not in _products:
        raise HTTPException(status_code=404, detail="Product not found")
    del _products[product_id]
