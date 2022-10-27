# Import the Flask class from the flask library
from winreg import HKEY_LOCAL_MACHINE
from flask import Flask, abort, request #external dependency
import json #internal dependency
from config import me, db
from mock_data import catalog

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
    cursor = db.products.find({})
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
    total=0
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
    for prod in catalog:
        if str.lower(prod["category"]) == str.lower(category):
            results.append(prod)
    
    return json.dumps(results)

# get /api/catalog/lower/<amount>
# show those lower than amount
@app.get("/api/catalog/lower/<amount>")
def lower_then(amount):
    results = []
    for prod in catalog:
        if prod["price"] < float(amount):
            results.append(prod)
    return json.dumps(results)

# get /api/category/unique
# get the list of unique categories
@app.get("/api/category/unique")
def categories_list():
    categories = []
    for prod in catalog:
        category = prod["category"]
        if not category in categories :
            categories.append(category)
    
    return json.dumps(categories)

@app.get("/api/test/colors")
def unique_color():
    colors = ["red", 'blue',"Pink", "yelloW", "Red", "Black", "BLUE", "RED", "BLACK", "YELLOW"]
    results = []
    for color in colors:
        color = str.lower(color)
        if color not in results:
            results.append(color)
    
    return json.dumps(results)

@app.get("/api/test/count/<color>")
def count_color(color):
    colors = ["red", 'blue',"Pink", "yelloW", "Red", "Black", "BLUE", "RED", "BLACK", "YELLOW"]

    # parse your color to lower
    color = color.lower()
    # return the number of times the color appears in the list
    counter = 0
    for c in colors:
        c = c.lower()
        if color == c:
            counter += 1
    return json.dumps(counter)
# run the app in debug mode
app.run(debug=True)
# When in production, turn off debug mode