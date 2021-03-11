from fastapi import FastAPI
# from pydantic_v import TestPostValidate
from pydantic import BaseModel
from typing import Optional, List

# for debug import uvicorn
import uvicorn





# make FastAPI instance with name app
app = FastAPI()




# DO CRUD WITHOUT DATABASE
# Run - uvicorn module_name:app --reload
# start first api with get operation

@app.get('/')  # know as path operation decorator (path('/'), operation(get()), decorator @)
def home(): # know as path operator function
    return {'hello': 'Hello FastAPI'}

# get with parameter
@app.get('/home/')
def show_book(limit: int=10): # limiting data for response
    return {"result": f"successfull get request"}

# post request (send data from client)
# we can validate sended data from client in function parameter
@app.post('/home/')
def create_book(name: str, age: int, location: str):
    return {"result": f" post request from user name-{name} and location-{location}"}

# same
# or validating data sended from client, using pydantic -- BaseModel
# use to request body use pydantic
class TestPostValidate(BaseModel):
    id: int
    name: str
    location: Optional[str]=None
    price: float
    book_rent: List[str]=[]

@app.post('/home/post/validate')
def create_book_py(book_item_request : TestPostValidate):
    return {"book rend" : book_item_request}



# if __name__ == '__main__':
#     uvicorn.run(app=app, host="127.0.0.1", port=9000 )








