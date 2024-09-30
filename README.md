# FastAPI Application

## Overview

This FastAPI application provides several endpoints to manage products and shopping carts. It includes functionalities to fetch and sort products, manage shopping carts, and handle checkout processes using the Stripe Python library.

## Features

1. **Fetch and Save Products**
   - Fetch a list of products from an external API.
   - Sort products in ascending or descending order by price.
   - Save the JSON response on the server as [`products.json`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fmgfos207%2FDesktop%2FMFORSTER_FREELANCE%2FInterviews%2FOneSeven_Tech%2Fproducts.json%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%225c68c381-788a-41e0-96a9-54971301884a%22%5D "/home/mgfos207/Desktop/MFORSTER_FREELANCE/Interviews/OneSeven_Tech/products.json").

2. **Get Shopping Cart**
   - Fetch the shopping cart of a user by user ID from `fakestoreapi.com/{user_id}`.
   - Add prices to the products in the shopping cart by cross-referencing with [`products.json`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fmgfos207%2FDesktop%2FMFORSTER_FREELANCE%2FInterviews%2FOneSeven_Tech%2Fproducts.json%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%225c68c381-788a-41e0-96a9-54971301884a%22%5D "/home/mgfos207/Desktop/MFORSTER_FREELANCE/Interviews/OneSeven_Tech/products.json").
   - Include a sum total for each of the user's shopping carts.

3. **Shopping Cart CRUD Operations**
   - Create, Read, Update, and Delete shopping carts using `fakestoreapi.com/cart` as the data source.
   - Return the response as JSON.

4. **Checkout Endpoint**
   - Enable user cart checkout using the Stripe Python library.
   - Fetch cart data using the local get cart API endpoint.
   - Filter the response to use the cart based on the ID used in the checkout request parameter.
   - Return a success message if the payment is successful.

## Endpoints

### 1. Fetch and Save Products

- **GET /products**
  - Fetch products from the external API.
  - Query Parameters: `sort` (optional, values: `asc`, `desc`).
  - Save the response as [`products.json`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fmgfos207%2FDesktop%2FMFORSTER_FREELANCE%2FInterviews%2FOneSeven_Tech%2Fproducts.json%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%225c68c381-788a-41e0-96a9-54971301884a%22%5D "/home/mgfos207/Desktop/MFORSTER_FREELANCE/Interviews/OneSeven_Tech/products.json").

### 2. Get Shopping Cart

- **GET /cart/{user_id}**
  - Fetch the shopping cart of a user by user ID.
  - Add prices to the products in the cart.
  - Include a sum total for each cart.

### 3. Shopping Cart CRUD Operations

- **POST /cart**
  - Create a new shopping cart.
  - Request Body: JSON object representing the cart.

- **GET /cart**
  - Fetch all shopping carts.

- **GET /cart/{cart_id}**
  - Fetch a specific shopping cart by cart ID.

- **PUT /cart/{cart_id}**
  - Update a specific shopping cart by cart ID.
  - Request Body: JSON object representing the updated cart.

- **DELETE /cart/{cart_id}**
  - Delete a specific shopping cart by cart ID.

### 4. Checkout Endpoint

- **POST /checkout**
  - Enable user cart checkout using Stripe.
  - Request Parameters: `cart_id`, [`user_id`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fhome%2Fmgfos207%2FDesktop%2FMFORSTER_FREELANCE%2FInterviews%2FOneSeven_Tech%2Ftest_takehome.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A3%2C%22character%22%3A124%7D%7D%5D%2C%225c68c381-788a-41e0-96a9-54971301884a%22%5D "Go to definition").
  - Return a success message if the payment is successful.

## Setup

1. Clone the repository.
2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the FastAPI application:
   ```sh
   uvicorn main:app --reload
   ```

## Dependencies

- FastAPI
- Stripe Python library
- Requests

## License

This project is licensed under the MIT License.