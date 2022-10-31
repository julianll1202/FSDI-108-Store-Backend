# Import the Flask class from the flask library
from flask import Flask, abort, request  # external dependency
import json  # internal dependency
from config import me, db
from mock_data import catalog
from bson import ObjectId
# Create a new app
app = Flask("Server")

# When you receive a get request at the root endpoint
# execute the home function


@app.get("/")
def home():
    return "Hello from my Flask server"


@app.get("/test")
def test():
    return "This is a test page"


@app.get("/about")
def about():
    return "Julian Lopez"

##################################################
#               API ENDPOINTS
# From this point, you will only work with json
##################################################


@app.get("/api/version")
def version():
    v = {
        "version": "1.0.0",
        "build": 8,
        "name": "Vainilla",
        "developer": me
    }
    return json.dumps(v)


def fix_id(obj):
    obj["_id"] = str(obj["_id"])
    return obj

# get /api/catalog


@app.get("/api/catalog")
# return catalog as json
def catalogue():
    cursor = db.products.find({}).sort("title")
    results = []

    for prod in cursor:
        results.append(fix_id(prod))

    return json.dumps(results)


@app.post("/api/catalog")
def save_product():
    product = request.get_json()

    if product is None:
        return abort(400, "Product required")
    # Validate price, title, etc

    # database.collectioName.insert_one()
    db.products.insert_one(product)
    print("-----------------------------")
    print(product)
    print("-----------------------------")

    # Changes the name of the category to lower case
    product["category"] = product["category"].lower()
    # Changes the object id to something manageable by
    # the Python server
    product["_id"] = str(product["_id"])

    return json.dumps(product)

# get /api/products/count
# return the number of products in catalog


@app.get("/api/products/count")
def product_count():
    # A more efficient way
    count = db.products.count_documents({})

    # get the length of the list
    return json.dumps(count)

# get /api/products/total
# return the sum of all the prices


@app.get("/api/products/total")
def product_total():
    total = 0
    # cursor with the products
    cursor = db.products.find({})
    # travel the cursor
    for prod in cursor:
        total += prod["price"]

    return json.dumps(total)

# get /api/catalog/categoryName
# return all the products that belong to  that category


@app.get("/api/catalog/<category>")
def by_category(category):
    results = []
    cursor = db.products.find({"category": category})

    for prod in cursor:
        results.append(fix_id(prod))

    return json.dumps(results)

# get /api/catalog/lower/<amount>
# show those lower than amount


@app.get("/api/catalog/lower/<amount>")
def lower_then(amount):
    results = []
    cursor = db.products.find({"price": {"$lt": float(amount)}})
    for prod in cursor:
        results.append(fix_id(prod))

    return json.dumps(results)


@app.get("/api/catalog/greater/<amount>")
def greater_then(amount):
    results = []
    cursor = db.products.find({"price": {"$gte": float(amount)}})
    for prod in cursor:
        results.append(fix_id(prod))

    return json.dumps(results)


# get /api/category/unique
# get the list of unique categories
@app.get("/api/category/unique")
def categories_list():
    results = []
    cursor = db.products.distinct("category")
    for cat in cursor:
       results.append(cat)

    return json.dumps(results)

# updates the information on a specified product
@app.put("/api/catalog")
def update_product():
    product = request.get_json()
    id = product.pop("_id") #read and remove _id

    # deletes the id from product
    # del product["_id"]

    # Updates the info
    res = db.products.update_one({"_id":ObjectId(id)}, {"$set":product})

    return json.dumps("Ok")

# deletes a product from the catalog
@app.delete("/api/catalog/<id>")
def delete_product(id):
    res = db.products.delete_one({"_id":ObjectId(id)})
    return json.dumps({"count": res.deleted_count})

@app.get("/api/product/details/<id>")
def find_product(id):
    prod = db.products.find_one({"_id":ObjectId(id)})
    if prod:
        return json.dumps(fix_id(prod))

    return abort(404, "Product not found")
# @app.get("/api/test/colors")
# def unique_color():
#     colors = ["red", 'blue', "Pink", "yelloW", "Red",
#               "Black", "BLUE", "RED", "BLACK", "YELLOW"]
#     results = []
#     for color in colors:
#         color = str.lower(color)
#         if color not in results:
#             results.append(color)

#     return json.dumps(results)


# @app.get("/api/test/count/<color>")
# def count_color(color):
#     colors = ["red", 'blue', "Pink", "yelloW", "Red",
#               "Black", "BLUE", "RED", "BLACK", "YELLOW"]

#     # parse your color to lower
#     color = color.lower()
#     # return the number of times the color appears in the list
#     counter = 0
#     for c in colors:
#         c = c.lower()
#         if color == c:
#             counter += 1
#     return json.dumps(counter)


# run the app in debug mode
app.run(debug=True)
# When in production, turn off debug mode
