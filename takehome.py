"""
Generate fastapi endpoints using fakestoreapi.com as the data source. The endpoints should do the following operations:
1. Fetch list of products from the API that can be sorted in ascending or descending order by price. Then take the json response and save it on the server as a json file called products.json.
2. Create a get shopping cart endpoint that will return the shopping cart of a user by user id using the fakestopreapi.com/{user_id} to fetch the shopping carts associated with that user id. The shopping cart data currently doesn't have the price for the products in the shopping cart, add the price for the prodcuts by cross referencing the price for the product from the products.json file on the server add that price to the carts data. Lastly include a sum total for each of the user's shopping carts by going through each item in the cart taking its unit price and multiply it by how many product items are in the basket. It is important to note that there can be multiple carts associated with a user id. Treat each cart as a separate entity.
3. Create additional shopping cart endpoints for the CRUD operations using fakestopreapi.com/cart as the data source. Invoke the fakestoreapi cart CRUD operations in each of these endpoints and return the response as JSON.
4. Lastly create endpoints that will enable a user cart checkout using the stripe Python library. The cart ID and user ID should be passed to the endpoint. In order to get the cart data, use localhost's get cart API endpoint to fetch the cart data, then filter the response to only use the cart based on the id used in the checkout request parameter. The checkout endpoint should return a success message if the payment is successful.
"""
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import httpx
import json
import os
import stripe

from base_models import Cart

app = FastAPI()
BASE_URL = "https://fakestoreapi.com"
PRODUCTS_FILE = "products.json"
stripe.api_key = "sk_test_51Q46knEFQgJsDPbW9U6FJQTVp5UAZF6yzxO1eqafzMsYh6e6wUiqBS4V7nzhuZXV2FwxX7nsS8m0SqkZoe4PGPTK008zp0ApCy"

@app.get("/products")
async def get_products(order: Optional[str] = Query("asc", regex="^(asc|desc)$")):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/products")
        products = response.json()
        sorted_products = sorted(products, key=lambda x: x['price'], reverse=(order == "desc"))
        
        # Save the sorted products to products.json
        with open(PRODUCTS_FILE, "w") as f:
            json.dump(sorted_products, f)
        
        return sorted_products

@app.get("/carts/{user_id}")
async def get_cart(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/carts/user/{user_id}")
        user_carts = response.json()
    
    # Load products from products.json
    if not os.path.exists(PRODUCTS_FILE):
        raise HTTPException(status_code=500, detail="Products file not found")
    
    with open(PRODUCTS_FILE, "r") as f:
        products = json.load(f)
    
    product_map = {product['id']: product['price'] for product in products}
    for cart in user_carts:
        total_price = 0
        for item in cart['products']:
            if 'price' not in item:
                item['price'] = product_map[item['productId']]
            total_price += item['price'] * item['quantity']
        cart['total'] = total_price
    
    return user_carts

@app.post("/carts")
async def add_to_cart(cart: Cart):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/carts", json=cart.model_dump())
        return response.json()

@app.put("/carts/{cart_id}")
async def update_cart(cart_id: int, cart: Cart):
    print("Did we get here at least")
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{BASE_URL}/carts/{cart_id}", json=cart.model_dump())
        return response.json()

@app.delete("/carts/{cart_id}")
async def delete_cart(cart_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/carts/{cart_id}")
        return response.json()

@app.get("/checkout")
async def checkout(user_id: int, cart_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/carts/{user_id}")
        user_carts = response.json()
    
    # Find the cart by cart_id
    print(user_carts, "haha the cart")
    cart = next((c for c in user_carts if c['id'] == cart_id), None)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # Create a Stripe payment intent
    intent = stripe.PaymentIntent.create(
        amount=int(cart['total'] * 100),  # Stripe expects the amount in cents
        currency='usd',
        payment_method_types=['card'],
    )
    
    return {"message": "Payment successful", "client_secret": intent['client_secret']}