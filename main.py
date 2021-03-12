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

@app.get('/', tags=['FastAPI Basic'])  # know as path operation decorator (path('/'), operation(get()), decorator @)
def home(): # know as path operator function
    return {'hello': 'Hello FastAPI'}


# post request (send data from client)
# we can validate sended data from client in function parameter
# limit 10 will show 10 data at a time
@app.post('/home/', tags=['FastAPI Basic'])
def create_book(name: str, age: int, location: str, limit: int=10):
    return {"result": f" post request from user name-{name} and location-{location}"}

########################################################################################

# same
# or validating data sended from client(browser)
# using pydantic -- BaseModel
# use to request body use pydantic
class PostSchema(BaseModel):
    id: int
    name: str
    location: Optional[str]=None
    price: float
    book_rent: List[str]=[]

@app.post('/home/post/', tags=['FastAPI Use Schema'])
def create_book_py(book_item_request : PostSchema):
    print(book_item_request)
    return book_item_request



if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=9000 )








