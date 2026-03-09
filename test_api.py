"""Tests for the products CRUD routes in api.py."""

import pytest
from fastapi.testclient import TestClient

import api
from api import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_products():
    """Reset in-memory products store before each test."""
    api._products.clear()
    api._next_id = 1
    yield


# --- list products ---

def test_list_products_empty():
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


def test_list_products_returns_all():
    client.post("/products", json={"name": "Apple", "price": 1.0})
    client.post("/products", json={"name": "Banana", "price": 0.5})
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 2


# --- get product by id ---

def test_get_product_not_found():
    response = client.get("/products/999")
    assert response.status_code == 404


def test_get_product_found():
    created = client.post("/products", json={"name": "Apple", "price": 1.0}).json()
    response = client.get(f"/products/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Apple"


# --- create product ---

def test_create_product():
    response = client.post(
        "/products",
        json={"name": "Cherry", "description": "Sweet fruit", "price": 3.0},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Cherry"
    assert data["description"] == "Sweet fruit"
    assert data["price"] == 3.0


def test_create_product_increments_id():
    first = client.post("/products", json={"name": "A", "price": 1.0}).json()
    second = client.post("/products", json={"name": "B", "price": 2.0}).json()
    assert second["id"] == first["id"] + 1


# --- update product ---

def test_update_product():
    created = client.post("/products", json={"name": "Old", "price": 1.0}).json()
    response = client.put(
        f"/products/{created['id']}",
        json={"name": "New", "price": 9.99},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New"
    assert response.json()["price"] == 9.99


def test_update_product_not_found():
    response = client.put("/products/999", json={"name": "X", "price": 1.0})
    assert response.status_code == 404


# --- delete product ---

def test_delete_product():
    created = client.post("/products", json={"name": "Temp", "price": 0.1}).json()
    response = client.delete(f"/products/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/products/{created['id']}").status_code == 404


def test_delete_product_not_found():
    response = client.delete("/products/999")
    assert response.status_code == 404
