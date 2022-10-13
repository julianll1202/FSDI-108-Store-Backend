# Import the Flask class from the flask library
from winreg import HKEY_LOCAL_MACHINE
from flask import Flask #external dependency
import json #internal dependency
from config import me, hello
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
    hello()
    return json.dumps(v)

# get /api/catalog
@app.get("/api/catalog")
# return catalog as json
def catalogue():
    return json.dumps(catalog)

# get /api/products/count
# return the number of products in catalog
@app.get("/api/products/count")
def product_count():
    return json.dumps(len(catalog))
# run the app in debug mode
app.run(debug=True)
# When in production, turn off debug mode