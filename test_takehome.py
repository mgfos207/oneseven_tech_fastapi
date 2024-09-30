"""
Generate unit tests based on the following requirements for a fastapi application:
1. Fetch list of products from the API that can be sorted in ascending or descending order by price. Then take the json response and save it on the server as a json file called products.json.
2. Create a get shopping cart endpoint that will return the shopping cart of a user by user id using the fakestopreapi.com/{user_id} to fetch the shopping carts associated with that user id. The shopping cart data currently doesn't have the price for the products in the shopping cart, add the price for the prodcuts by cross referencing the price for the product from the products.json file on the server add that price to the carts data. Lastly include a sum total for each of the user's shopping carts by going through each item in the cart taking its unit price and multiply it by how many product items are in the basket. It is important to note that there can be multiple carts associated with a user id. Treat each cart as a separate entity.
3. Create additional shopping cart endpoints for the CRUD operations using fakestopreapi.com/cart as the data source. Invoke the fakestoreapi cart CRUD operations in each of these endpoints and return the response as JSON.
4. Lastly create endpoints that will enable a user cart checkout using the stripe Python library. The cart ID and user ID should be passed to the endpoint. In order to get the cart data, use localhost's get cart API endpoint to fetch the cart data, then filter the response to only use the cart based on the id used in the checkout request parameter. The checkout endpoint should return a success message if the payment is successful.
"""
import json
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from takehome import app  # Assuming your FastAPI app is in a file named main.py
from base_models import Cart
client = TestClient(app)

# Helper function to load JSON data from a file
def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Test fetching list of products
def test_get_products():
    response = client.get("/products?order=asc")
    assert response.status_code == 200
    products = response.json()
    assert products == sorted(products, key=lambda x: x['price'])

    response = client.get("/products?order=desc")
    assert response.status_code == 200
    products = response.json()
    assert products == sorted(products, key=lambda x: x['price'], reverse=True)

    # Verify products.json is saved
    assert os.path.exists("products.json")
    saved_products = load_json("products.json")
    assert saved_products == products

# Test getting shopping cart
def test_get_cart():
    response = client.get("/carts/1")
    assert response.status_code == 200
    carts = response.json()
    assert len(carts) == 2
    assert carts[0]['total'] == 798.04

# Test adding to cart
# @patch("httpx.AsyncClient.post")
def test_add_to_cart():
    # mock_post.return_value.json.return_value = {"message": "Product added to cart", "cart": {}}
    cart_data = {
    "id": 2,
    "userId": 1,
    "date": "2020-01-02T00:00:00.000Z",
    "products": [
      {
        "productId": 1,
        "quantity": 5
      },
      {
        "productId": 2,
        "quantity": 10
      },
      {
        "productId": 3,
        "quantity": 61
      }
   ]
  }
    add_cart_data = Cart(**cart_data)
    response = client.post("/carts", json=add_cart_data.model_dump())
    assert response.status_code == 200

# Test updating cart
def test_update_cart():
    cart = {"id": 11,"userId": 1,"date": "2020-01-02T00:00:00.000Z","products": [{"productId": 1,"quantity": 5},{"productId": 2,"quantity": 10},{"productId": 3,"quantity": 61}]}
    cart_data = Cart(**cart)
    response = client.put("/carts/11", json=cart_data.model_dump())
    assert response.status_code == 200

# Test deleting from cart
def test_delete_cart():
    response = client.delete("/carts/1")
    assert response.status_code == 200

# Test checkout
def test_checkout():
    response = client.get("/checkout", params={"user_id": 1, "cart_id": 1})
    assert response.status_code == 200