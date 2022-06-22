from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel


app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

inventory = {}

# pat/endpoint parameter
@app.get("/get-item/{item_id}")
def get_item(item_id: int=Path(None, description="The ID of the item")):
    return inventory[item_id]


# query parameter (if we set the default to None, it will work if parameter is not passed)
@app.get("/get-by-name")
def get_item_by_name(name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    return {"data": "Not found"}


# request body / post method
@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"error": "item already exists"}
    inventory[item_id] = item
    return inventory[item_id]


# update method (update function will change only the added (changed) parameters))
@app.put("/update/{item_id}")
def update(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"error": "no such element"}

    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]

@app.get("/")
def home():
    return {"data": "Testing"}

@app.get("/about")
def about():
    return {"data": "About"}