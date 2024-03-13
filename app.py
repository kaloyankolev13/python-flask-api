from flask import Flask, request
from flask_smorest import abort
import uuid
from db import stores, items
app = Flask(__name__)



@app.get('/store')
def get_stores():
    return {"stores": list(stores.values())}

@app.post('/store')
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400,
            message= "The request is invalid.Ensure the name is included in the request"
        )
    for store in stores.values():
        if store["name"] == store_data["name"]:
            return {"message": "Store already exists"}, 400
    store_id = uuid.uuid4().hex
    store = {
        **store_data,
        "id": store_id,
    }
    stores[store_id] = store
    return  store,201

@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return abort(404, {"message": "Store not found"})


@app.get('/item')
def get_items():
    return {"items": list(items.values())}

@app.post('/item')
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message= "The request is invalid. Ensure the name, price and store_id are included in the request.",
        )

    for item in items.values():
        if item["name"] == item_data["name"]:
            return {"message": "Item already exists"}, 400

    if (item_data["store_id"] not in stores):
        return {"message": "Store not found"}, 404
    item_id = uuid.uuid4().hex
    item = {
        **item_data,
        "id": item_id,
    }
    items[item_id] = item
    return item, 201

@app.get('/store/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Store not found"}, 404
    


if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True)