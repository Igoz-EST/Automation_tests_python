import pytest
import requests
import json
import random
import string

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


def test_can_post_to_search_product():

    payload = {"search_product": "tshirt"}
    response = requests.post(ENDPOINT + "/searchProduct", data=payload)
    data = response.json()
    product_list = data["products"]
    assert data["responseCode"] == 200
    for product in product_list:
       category = product["category"]
       assert category["category"] == 'Tshirts', "Response has not only Tshirts"

## --------------- API 6: POST To Search Product without search_product parameter ---------------

def test_can_post_to_search_product_without_search_parameter():
    response = requests.post(ENDPOINT + "/searchProduct")
    data = response.json()
    assert data["responseCode"] == 400
    assert data["message"] == "Bad request, search_product parameter is missing in POST request."


## --------------- API 7: POST To Verify Login with valid details ---------------

def test_can_post_to_verify_login_valid_details():
    payload = {
               "email": "milo@mail.com",
               "password": "123123"
               }
    response = requests.post(ENDPOINT + "/verifyLogin", data=payload)
    data = response.json()
    assert data["responseCode"] == 200
    assert data["message"] == "User exists!"

## --------------- API 8: POST To Verify Login without email parameter ---------------

def test_can_post_to_verify_login_without_parameter():
    payload = {
               "password": "123123"
               }
    response = requests.post(ENDPOINT + "/verifyLogin", data=payload)
    data = response.json()
    assert data["responseCode"] == 400
    assert data["message"] == "Bad request, email or password parameter is missing in POST request."

## --------------- API 9: DELETE To Verify Login ---------------

def test_can_delete_to_verify_login():
    response = requests.delete(ENDPOINT + "/verifyLogin")
    data = response.json()
    assert data["responseCode"] == 405
    assert data["message"] == "This request method is not supported."

## --------------- API 10: POST To Verify Login with invalid details ---------------

def test_can_post_to_verify_login_invalid_details():
    payload = {
               "email": "asdasd",
               "password": 123
               }
    response = requests.post(ENDPOINT + "/verifyLogin", data=payload)
    data = response.json()
    assert data["responseCode"] == 404
    assert data["message"] == "User not found!"

## --------------- API 11: POST To Create/Register User Account ---------------

def generate_random_string_without_repeats(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.sample(characters, k=length))
    return random_string

random_email = generate_random_string_without_repeats(10)

def test_can_post_to_create_user_account():

    payload = {
               "name": "Ivanchik",
               "email": f'{random_email}@mail.com',
               "password": "123123",
               "title": "Mr",
               "birth_date": "17",
               "birth_month": "06",
               "birth_year": "1999",
               "firstname": "Ivan",
               "lastname": "Ivanov",
               "company": "IvanCompany",
               "address1": "Ivan-45",
               "address2": "Ivan-46",
               "country": "Ivan",
               "zipcode": "Ivan",
               "state": "Ivan",
               "city": "Ivan",
               "mobile_number": "+37258495837",
               }
    response = requests.post(ENDPOINT + "/createAccount", data=payload)
    data = response.json()
    assert data["responseCode"] == 201
    assert data["message"] == "User created!"

## --------------- API 12: DELETE METHOD To Delete User Account ---------------

@pytest.fixture
def random_email():
    characters = string.ascii_letters + string.digits
    email = ''.join(random.choices(characters, k=10)) + "@mail.com" ## GEnerating the random email
    return email

@pytest.fixture
def test_create_user(random_email): ## Passing the random email to the test_create_user fixture
    payload = {
               "name": "Ivanchik",
               "email": random_email,
               "password": "password",
               "title": "Mr",
               "birth_date": "17",
               "birth_month": "06",
               "birth_year": "1999",
               "firstname": "Ivan",
               "lastname": "Ivanov",
               "company": "IvanCompany",
               "address1": "Ivan-45",
               "address2": "Ivan-46",
               "country": "Ivan",
               "zipcode": "Ivan",
               "state": "Ivan",
               "city": "Ivan",
               "mobile_number": "+37258495837",
               }
    requests.post(ENDPOINT + "/createAccount", data=payload)
    return payload["email"] ## Can i return more than 2 values? how will it look like?

@pytest.fixture
def test_can_post_to_delete_user_account(test_create_user): ## test_create_user fixture is returning the random email
     payload = {
               "email": test_create_user, ## Variable name is shit, i know. I will fix it after finishing the exam.
               "password": "password",
               }
     response = requests.delete(ENDPOINT + "/deleteAccount", data=payload) ## Deleting the user with the generated email
     data = response.json()
     assert data["responseCode"] == 200
     assert data["message"] == "Account deleted!"
     yield test_create_user ## Stoping the fixture executing and return the random email back to the test function


def test_user_not_exist(test_can_post_to_delete_user_account):
    email = test_can_post_to_delete_user_account
    payload = {
               "email": email,
               "password": "password"
               }
    response = requests.post(ENDPOINT + "/verifyLogin", data=payload)
    data = response.json()
    assert data["responseCode"] == 404
    assert data["message"] == "User not found!"

## --------------- API 13: PUT METHOD To Update User Account ---------------

@pytest.fixture
def test_create_user_for_update(random_email): ## Passing the random email to the test_create_user fixture
    payload = {
               "name": "Ivanchik",
               "email": random_email,
               "password": "password",
               "title": "Mr",
               "birth_date": "17",
               "birth_month": "06",
               "birth_year": "1999",
               "firstname": "Ivan",
               "lastname": "Ivanov",
               "company": "IvanCompany",
               "address1": "Ivan-45",
               "address2": "Ivan-46",
               "country": "Ivan",
               "zipcode": "Ivan",
               "state": "Ivan",
               "city": "Ivan",
               "mobile_number": "+37258495837",
               }
    requests.post(ENDPOINT + "/createAccount", data=payload)
    return payload["email"] ## Can i return more than 2 values? how will it look like?

@pytest.fixture
def test_user_not_exist(test_create_user_for_update):
    email = test_create_user_for_update
    payload = {
               "email": email
               }
    response = requests.post(ENDPOINT + "/getUserDetailByEmail", data=payload)
    data = response.json()
    assert data["responseCode"] == 200
    assert data["message"] == "User not found!"
