"""
Note that this does not have an entry point function main().

Instead your run fastapi dev main.py

The composition is:
-  this main.py gets imported in a uvicorn server.
-  the unvicorn server is run
-  the fast api program does UI magic with the terminal 

"""

from enum import Enum
from typing import Annotated, Literal

from fastapi import FastAPI, Query  
from pydantic import BaseModel, Field

from fastapi.testclient import TestClient
import uvicorn


app = FastAPI()

"""
You can use an enum as validation spec for a param.
Note multiple inheritance.
Inheriting from str provides formatting for JSON.
"""
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/")
async def root():
    return {"message": "Hello World"}

"""
Passing parsed URL params into handler.
On Ok get json type conversion (to int).
On Err get cute validation error details.
"""
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


"""
Shows validation against an Enum.
"""
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

"""
Query parameters are implicitly defined (and typed) by the handler.
Note also default values.
The handler receives them type converted from the natural url sub-strings.
Aside - recall that python returns empty list when slice index out of bounds .
"""
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

"""
Type format and interpretation for an option param (q).
"""
@app.get("/abc/{abc_id}")
async def read_abc(abc_id: str, q: str | None = None):
    if q:
        return {"abc_id": abc_id, "q": q}
    return {"abc_id": abc_id}


"""
Read request body (for POST) using a pydantic.BaseModel
"""
class Widget(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
@app.post("/widgets/")
async def create_widget(widget: Widget):
    return widget


"""
If you wrap types with Annotated, you get access to new forms of validation.
See VSCode intellisense to see other forms for Query.
E.g. gt/lt, and "match" (regex).
"""
@app.get("/annotated/")
async def annotated(q: Annotated[str | None, Query(max_length=4)] = None):
    if q:
        return {"q_value": q}
    return {"q_value": "n/a"}

"""
Notes on Annotated Query and Path

You would struggle to define a query param called "item-query" because
the argument to the function would then have an illegal name.
But you can achieve that by aliasing it:
    read_items(q: Annotated[str | None, Query(alias="item-query")] = None)

See also the Path alt to Query for similar semantics.
"""


"""
Modelling using nested pydantic models and native container types.
"""
class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None

@app.put("/nested_models/{item_id}")
async def update_nested(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

    """
    Some extra features to explore

    - Declare default values for requests.
    - Less common supported types like: DateTime, UUID.
    - You can define a request input as of type Cookie.
    - Or specify a group of Cookies using a Pydantic model.
    - You can define a request input as of type Header [filed expected in header]
    - You can modelise the Response.
    - You can specify that a handler expects a file input.
    - You signal errors from handler logic by raising a fastAPI.HTTPException.
    - Direct support for all kinds of auth.
    - Custom middleware - like timing the handler.
    - CORS middleware - most APIs likely need to all the "*" origin.
    - Fabulous looking SQL database ORM (first-class) integration
    - Post response background tasks.
    - Static files  
    
    """

"""
Play around with testing
"""
def test_plain_python():
        assert 3 == 3

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}






"""
Use this form below if you want to use the debugger easily in
VSCode

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
