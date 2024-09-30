"""
Generate unit tests based on the following requirements for a fastapi application:
1. Fetch list of products from the API that can be sorted in ascending or descending order by price. Then take the json response and save it on the server as a json file called products.json.
2. Create a get shopping cart endpoint that will return the shopping cart of a user by user id using the fakestopreapi.com/{user_id} to fetch the shopping carts associated with that user id. The shopping cart data currently doesn't have the price for the products in the shopping cart, add the price for the prodcuts by cross referencing the price for the product from the products.json file on the server add that price to the carts data. Lastly include a sum total for each of the user's shopping carts by going through each item in the cart taking its unit price and multiply it by how many product items are in the basket. It is important to note that there can be multiple carts associated with a user id. Treat each cart as a separate entity.
3. Create additional shopping cart endpoints for the CRUD operations using fakestopreapi.com/cart as the data source. Invoke the fakestoreapi cart CRUD operations in each of these endpoints and return the response as JSON.
4. Lastly create endpoints that will enable a user cart checkout using the stripe Python library. The cart ID and user ID should be passed to the endpoint. In order to get the cart data, use localhost's get cart API endpoint to fetch the cart data, then filter the response to only use the cart based on the id used in the checkout request parameter. The checkout endpoint should return a success message if the payment is successful.
"""
import pytest
import httpx
from fastapi.testclient import TestClient
from respx import MockRouter
from takehome import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_get_products_sorted_asc(respx_mock: MockRouter):
    mock_response = [
        {"id": 1, "price": 10.0},
        {"id": 2, "price": 5.0},
        {"id": 3, "price": 15.0}
    ]
    respx_mock.get("https://fakestoreapi.com/products").mock(return_value=httpx.Response(200, json=mock_response))

    response = client.get("/products?order=asc")
    assert response.status_code == 200
    assert response.json() == sorted(mock_response, key=lambda x: x['price'])

@pytest.mark.asyncio
async def test_get_products_sorted_desc(respx_mock: MockRouter):
    mock_response = [
        {"id": 1, "price": 10.0},
        {"id": 2, "price": 5.0},
        {"id": 3, "price": 15.0}
    ]
    respx_mock.get("https://fakestoreapi.com/products").mock(return_value=httpx.Response(200, json=mock_response))

    response = client.get("/products?order=desc")
    assert response.status_code == 200
    assert response.json() == sorted(mock_response, key=lambda x: x['price'], reverse=True)

@pytest.mark.asyncio
async def test_get_cart(respx_mock: MockRouter):
    mock_cart = [{
        "id": 1,
        "userId": 1,
        "products": [
            {"productId": 1, "quantity": 2, "product": {"price": 10.0}},
            {"productId": 2, "quantity": 1, "product": {"price": 5.0}}
        ]
    }]
    respx_mock.get("https://fakestoreapi.com/carts/user/1").mock(return_value=httpx.Response(200, json=mock_cart))

    response = client.get("/carts/1")
    assert response.status_code == 200
    assert response.json() == {
        "cart": mock_cart,
        "total_price": 25.0
    }

@pytest.mark.asyncio
async def test_add_to_cart(respx_mock: MockRouter):
    mock_cart = {
        "id": 1,
        "userId": 1,
        "products": []
    }
    updated_cart = {
        "id": 1,
        "userId": 1,
        "products": [{"productId": 1, "quantity": 2}]
    }
    respx_mock.get("https://fakestoreapi.com/carts/user/1").mock(return_value=httpx.Response(200, json=mock_cart))
    respx_mock.put("https://fakestoreapi.com/carts/1").mock(return_value=httpx.Response(200, json=updated_cart))

    response = client.post("/carts/1/add", params={"product_id": 1, "quantity": 2})
    assert response.status_code == 200
    assert response.json() == {"message": "Product added to cart"}

@pytest.mark.asyncio
async def test_update_cart(respx_mock: MockRouter):
    mock_cart = {
        "id": 1,
        "userId": 1,
        "products": [{"productId": 1, "quantity": 2}]
    }
    updated_cart = {
        "id": 1,
        "userId": 1,
        "products": [{"productId": 1, "quantity": 3}]
    }
    respx_mock.get("https://fakestoreapi.com/carts/user/1").mock(return_value=httpx.Response(200, json=mock_cart))
    respx_mock.put("https://fakestoreapi.com/carts/1").mock(return_value=httpx.Response(200, json=updated_cart))

    response = client.put("/carts/1/update", params={"product_id": 1, "quantity": 3})
    assert response.status_code == 200
    assert response.json() == {"message": "Cart updated"}