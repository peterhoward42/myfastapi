from fastapi import FastAPI
from enum import Enum

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
