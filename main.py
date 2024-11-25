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