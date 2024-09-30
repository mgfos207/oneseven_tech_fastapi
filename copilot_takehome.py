from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict, Optional
import httpx
import json
import os
import stripe

app = FastAPI()
BASE_URL = "https://fakestoreapi.com"
PRODUCTS_FILE = "products.json"
stripe.api_key = "your_stripe_secret_key"

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
            item['price'] = product_map[item['productId']]
            total_price += item['price'] * item['quantity']
        cart['total'] = total_price
    
    return user_carts

@app.post("/carts")
async def add_to_cart(cart: Dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/carts", json=cart)
        return response.json()

@app.put("/carts/{cart_id}")
async def update_cart(cart_id: int, cart: Dict):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{BASE_URL}/carts/{cart_id}", json=cart)
        return response.json()

@app.delete("/carts/{cart_id}")
async def delete_cart(cart_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/carts/{cart_id}")
        return response.json()

@app.post("/checkout")
async def checkout(user_id: int, cart_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/carts/{user_id}")
        user_carts = response.json()
    
    # Find the cart by cart_id
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