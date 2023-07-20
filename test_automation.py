import requests
import json


ENDPOINT = "https://automationexercise.com/api"

## --------------- API 1: Get All Products List ---------------

def test_can_get_all_products():
    response = requests.get(ENDPOINT + "/productsList")
##    assert response.status_code == 200 ## Checking for the needed status code
    data = response.json()
   ## print(data)
    assert data is not None and data != {} , "Data is absent"
    assert "products" in data, "products was not found" ## checking, that data in response has the "products" object
    products_list = data["products"] ## Writing the "products" object from the response into "products_list" variable, to use it in the for cycle
    for product in products_list: ## Checking the keys in the response, using the "for" cycle
        ## Checking, that fields are exist:
        assert "id" in product, "key 'id' was not found"
        assert "name" in product, "key 'name' was not found"
        assert "price" in product, "key 'price' was not found"
        assert "brand" in product, "key 'brand' was not found"
        assert "category" in product, "key 'category' was not found"

        category = product.get("category") ## Checking the keys in the nested objects
        assert category is not None, "Object Category was not found"
        assert "usertype" in category, "key 'usertype' was not found"
        assert "category" in category, "key 'Category' was not found"
        ## Checking the data type:
        assert isinstance(product["id"], int), "Key 'id' is not of type 'int'"
        assert isinstance(product["name"], str), "Key 'name' is not of type 'str'"
        assert isinstance(product["price"], str), "Key 'price' is not of type 'float'"
        assert isinstance(product["brand"], str), "Key 'brand' is not of type 'str'"
        assert isinstance(product["category"], object), "Key 'category' is not of type 'object'"

        userType = category.get("usertype")

        assert "usertype" in category, "key 'usertype' was not found"
        assert "usertype" in userType, "key 'usertype' was not found"
        assert isinstance(category["usertype"], object), "Key 'usertype' is not of type 'object'"
        assert isinstance(userType["usertype"], object), "Key 'usertype' is not of type 'object'"
        sex = userType.get("usertype") ##Getting the user

        assert sex in ["Kids", "Women", "Men", "Attack-helicopter"], "Key 'usertype' is not within allowed range" ## Kids it's a third gender lol

## --------------- API 2: POST To All Products List ---------------

def test_can_all_products_list():
    response = requests.post(ENDPOINT + "/productsList")
##    assert response.status_code == 200 ## Checking for the needed status code
    data = response.json()
    assert data["responseCode"] == 405
    assert data["message"] == "This request method is not supported."

## --------------- API 3: Get All Brands List ---------------

def test_can_get_brands_list():
    response = requests.get(ENDPOINT + "/brandsList")
 ##   assert response.status_code == 200 ## Checking for the needed status code
    data = response.json()
    assert data["brands"] != None and data["brands"] != {}, "Brands are empty"
    brands_list = data["brands"]
    for brand in brands_list:
        assert "id" in brand, "key 'id' was not found"
        assert "brand" in brand, "key 'brand' was not found"
        assert brand["id"] is not None and brand["id"] != "", "Value in 'id' key is empty or not exist"
        assert brand["brand"] is not None and brand["brand"] != "", "Value in 'brand' key is empty or not exist"


## --------------- API 4: PUT To All Brands List ---------------

def test_can_put_to_all_brands():
    response = requests.put(ENDPOINT + "/brandsList")
    data = response.json()
    assert data["responseCode"] == 405
    assert data["message"] == "This request method is not supported."


## --------------- API 5: POST To Search Product ---------------



## def test_can_search_product():


