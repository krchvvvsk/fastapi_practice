from fastapi import FastAPI,Query,Path

app = FastAPI()

@app.get('/hello')
def say_hello():
    return {"message": "Hello, FastApi!"}

@app.get("/users/{user_id}")
def get_user(user_id:int):
    return {
        "message": "User found",
        "id": user_id
    }

# @app.get("/products/{product_id}")
# def get_product(product_id:int, limit:int = 10):
#     return {
#         "message": "Product Found",
#         "product_id" : product_id,
#         "limit": limit
#     }

# @app.get("/products")
# def get_products(category: str):
#     return {"category": category}

@app.get("/products/{product_id}")
def get_product(product_id: int=Path(ge=1,description="Unique product identifier"),limit: int=Query(default=20,ge=1,le=50,description="Maximum number of products to return")):
    return{
        "message": "Product Found",
        "product_id":product_id,
        "limit":limit
    }