import requests
import json


ENDPOINT = "https://automationexercise.com/api"

## --------------- API 1: Get All Products List ---------------

def test_can_get_all_products():
    response = requests.get(ENDPOINT + "/productsList")
    assert response.status_code == 200 ## Checking for the needed status code
    data = response.json()
    assert data is not None and data != {} , "Data is absent"
    assert "products" in data, "products was not found" ## checking, that data in response has the "products" object
    products_list = data["products"] ## Writing the "products" object from the response into "products_list" variable, to use it in the for cycle
    for product in products_list: ## Checking the keys in the response, using the "for" cycle
        assert "id" in product, "key 'id' was not found"
        assert "name" in product, "key 'name' was not found"
        assert "price" in product, "key 'price' was not found"
        assert "brand" in product, "key 'brand' was not found"
        assert "category" in product, "key 'category' was not found"

        category = product.get("category") ## Checking the keys in the nested objects
        assert category is not None, "Object Category was not found"
        assert "usertype" in category, "key 'usertype' was not found"
        assert "category" in category, "key 'Category' was not found"
    print("All tests were successfull")

## --------------- API 2: POST To All Products List ---------------

def test_can_all_products_list():
    response = requests.post(ENDPOINT + "/productsList")
    assert response.status_code == 200 ## Checking for the needed status code
    data = response.json()
    assert data["responseCode"] == 405
    assert data["message"] == "This request method is not supported."

## --------------- API 3: Get All Brands List ---------------

def test_can_get_brands_list():
    response = requests.get(ENDPOINT + "/brandsList")
    assert response.status_code == 200 ## Checking for the needed status code
    data = response.json()
    assert data["brands"] != None and data["brands"] != {}, "Brands are empty"
    brands_list = data["brands"]
    for brand in brands_list:
        assert "id" in brand, "key 'id' was not found"
        assert "brand" in brand, "key 'brand' was not found"
        assert brand["id"] is not None and brand["id"] != "", "Value in 'id' key is empty or not exist"
        assert brand["brand"] is not None and brand["brand"] != "", "Value in 'brand' key is empty or not exist"
    print("All tests were successfull")

## ------ the code below is experiments -----------

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    pass


##need a header parameter
def test_can_search_product():
    headers = {'User-Agent': 'My Custom User Agent', 'Content-Type': 'application/json'}
    search_product = "tshirt"
    payload = {"search_product": search_product}
    search_product = {'search_product': 'tshirt'}
    response = requests.post(ENDPOINT + "/searchProduct", headers=headers, json=payload, data=json.dumps(search_product))
    assert response.status_code == 200

    data = response.json()
    print(data)

