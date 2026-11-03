from fastapi import FastAPI,Query,Path,HTTPException
from pydantic import BaseModel,Field,field_validator

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


class Product(BaseModel):
    name: str = Field(min_length=1)
    @field_validator('name')
    @classmethod
    def space_validator(cls,name):
        name = name.strip()
        if len(name) == 0:
            raise ValueError("Invalid name")
        
        return name
        
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)
        

@app.post('/products',status_code=201)
def post_product(product: Product):
    return {
        "name":product.name,
        'price':product.price,
        'quantity':product.quantity
    }


products = {
    1: {"name": "Phone", "price": 500},
    2: {"name": "Laptop", "price": 1200}
}


@app.get('/produts/{produc_id}')
def product_check(produc_id: int = Path(gt=0)):
    inStockProduct = products.get(produc_id)
    if inStockProduct is not None:
        return inStockProduct
    else:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )



@app.put('/products/{product_id}')

def update_product(product:Product, product_id:int=Path(gt=0)):
    is_in_stock = products.get(product_id)
    if is_in_stock is not None:
        products[product_id]= product.model_dump()
        return products[product_id]
    raise HTTPException(
        status_code=404,
        detail="Product not updated"
    )



class ProductUpdate(BaseModel):
    name: str  | None = None
    
    @field_validator('name')
    @classmethod
    def space_remove(cls,name):
        if name is None:
            return name
        name = name.strip()
        if len(name) == 0 :
            raise ValueError('Invalid product name')
        return name
        
    price: float | None = None
    quantity: int | None = None


@app.patch('/products/{product_id}')
def patch_product(product:ProductUpdate,product_id:int=Path(gt=0)):
    is_in_stock = products.get(product_id)
    if is_in_stock is not None:
        products[product_id].update(product.model_dump(exclude_unset=True))
        return products[product_id]
    raise HTTPException(
        status_code=404,
        detail="Product not updated"
    )
        