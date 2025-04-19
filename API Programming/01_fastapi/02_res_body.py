"""

## Request Body in FastAPI
### Understanding Request Bodies

In API development, a request body is data sent by the client to your API. Request bodies are crucial when clients need to send larger structured data sets to the server.

The key points to understand:

- A response body is what your API sends back to clients
- A request body is what clients send to your API
- APIs always need to send response bodies, but clients don't always need to send request bodies
- POST requests typically include request bodies for creating or submitting data

"""

from fastapi import FastAPI
app = FastAPI()

@app.post('/adduser')
def adduser():
    return {'user': {'name': 'kirkyagami', 'email': 'kirkyagami99@gmail.com'}}

'''
This example defines a POST endpoint that doesn't yet process any incoming data - it simply returns a hardcoded user object. To actually process client data, we need to implement request body handling.
'''



from pydantic import BaseModel

class Profile(BaseModel):
    name: str
    email: str
    age: int

@app.post('/profile/')
def createprofile(profile: Profile):
    return profile


# ---====================================================================================

class Product(BaseModel):
	name: str
	price: int
	discount: int
	discounted_price: int



### Combining Request Bodies with Path Parameters

@app.post('/addproduct/{product_id}')
def addproduct(product: Product, product_id: int):
    product.discounted_price = product.price - (product.price * product.discount / 100)
    return {'product_id': product_id, 'product': product}

### Adding Query Parameters to the Mix

@app.post('/addproduct/{product_id}')
def addproduct(product: Product, product_id: int, category: str):
    product.discounted_price = product.price - (product.price * product.discount / 100)
    return {'product_id': product_id, 'product': product, 'category': category}



### Multiple Body Parameters




### Enhancing Models with Field Metadata


