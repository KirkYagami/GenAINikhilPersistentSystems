

""""
Creating our first API
"""

#importing the class from the module
from fastapi import FastAPI

# creating the app instance
app = FastAPI()

# API - something that accepts incoming requests from the client. How -> url is the request
# job of the API is to take the request and get back the appropriate resp



@app.get("/")
def index():
    return "Hii"


"""
path is also called as an endpoint or a route
get here is called as an operation, this is one of the HTTP methods.other such methods are post,put, delete, etc
get is used to get a resource/ data from api


def index here is called as a path operation function, this function will be called
by fast api whenever it receive a request to the URL '/' using a get operation.
"""


@app.get("/movies") # @ -> is the path operation decorator and its job is to associate the path with the func
def movies():
    return {"movies":["m1", "m2", "m3"]}


#  ==============================================


"""

Path parameters allow you to create dynamic routes in your API, making your endpoints more flexible and reusable. They're essential for RESTful API design and are commonly used to identify specific resources.

"""



@app.get('/property/{property_id}')
def get_property(property_id: int):
    return f"This is a page for property {property_id}"

# ----=========================================================


@app.get('/products/{product_id}')
def get_product_details(product_id: int):
    # In a real application, you would fetch the product from a database

    product = {
        "id": product_id,
        "name": f"Product {product_id}",
        "price": 29.99,
        "in_stock": True
    }
    return product


# https://tripadvisor-content-api.readme.io/reference/getlocationdetails


# ---

# ORDER MATTERS



@app.get('/user/{username}')
def profile(username):
    return {f' This is a profile page for {username} '}

@app.get('/user/admin')
def admin():
    return {'admin page'}

"""
## Query Parameters

Query parameters are used to filter, sort, or provide additional information to an API endpoint without being part of the resource identification. They're especially useful for optional parameters or when you need to include many parameters.

"""

@app.get('/products')
def products(id, price): # it's a query param, as it is not part of path
    return {f'Product ID: {id}'}


## Combining Path and Query Parameters

@app.get('/profile/{userid}/followers')
def profile(userid: int, device):
    return {f'Followers page for user {userid} and their followers are {device}'}





from typing import Optional

@app.get('/users/{user_id}/orders/')
def get_user_orders(
    user_id: int,
    status: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    # In a real application, you would fetch orders from a database
    filters = {
        "status": status,
        "date_range": {"from": from_date, "to": to_date},
        "pagination": {"page": page, "limit": limit}
    }
    
    return {
        "user_id": user_id,
        "filters_applied": filters,
        "total_orders": 42,
        "orders": [
            {"id": 1, "status": "delivered", "total": 99.99, "date": "2023-01-15"}
            # More orders would be here
        ]
    }





from pydantic import BaseModel
class Product(BaseModel):
	name: str
	price: int
	discount: int
	discounted_price: int


@app.post('/addproduct/{product_id}')
def addproduct(product: Product, product_id: int):
    product.discounted_price = product.price - (product.price * product.discount / 100)
    return {'product_id': product_id, 'product': product}




