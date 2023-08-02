import pytest
import requests
import json
import random
import string
from faker import Faker
import random

fake = Faker()

ENDPOINT = "https://automationexercise.com/api"

## --------------- API 1: Get All Products List ---------------

def test_can_get_all_products():
    response = requests.get(ENDPOINT + "/productsList")
##    assert response.status_code == 200 ## Checking for the needed status code
    data = response.json()
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
        assert brand["id"] is not None and brand["id"] != "", "Value in the 'id' key is empty or doesn't exist"
        assert brand["brand"] is not None and brand["brand"] != "", "Value in 'brand' key is empty or doesn't exist"


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
               "email": fake.email(),
               "password": 123
               }
    response = requests.post(ENDPOINT + "/verifyLogin", data=payload)
    data = response.json()
    assert data["responseCode"] == 404
    assert data["message"] == "User not found!"

## --------------- API 11: POST To Create/Register User Account ---------------
@pytest.fixture
def valid_titles():
    return ["Mr", "Mrs", "Miss"]

def test_can_post_to_create_user_account(valid_titles):
    mobile = "+" + fake.phone_number()
    name = fake.name()
    first_name, last_name = name.split()
    date = fake.date()
    year, month, day = date.split("-")
    title = random.choice(valid_titles)
    payload = {
               "name": name,
               "email": fake.email(),
               "password": fake.password(),
               "title": title,
               "birth_date": day,
               "birth_month": month,
               "birth_year": year,
               "firstname": first_name,
               "lastname": last_name,
               "company": fake.company(),
               "address1": fake.address(),
               "address2": fake.address(),
               "country": fake.country(),
               "zipcode": fake.zipcode(),
               "state": fake.state(),
               "city": fake.city(),
               "mobile_number": mobile,
               }
    response = requests.post(ENDPOINT + "/createAccount", data=payload)
    data = response.json()
    assert data["responseCode"] == 201
    assert data["message"] == "User created!"

## --------------- API 12: DELETE METHOD To Delete User Account ---------------

# @pytest.fixture
# def random_email():
#     characters = string.ascii_letters + string.digits
#     email = ''.join(random.choices(characters, k=10)) + "@mail.com" ## GEnerating the random email
#     return email

@pytest.fixture
def test_create_user(valid_titles): ## Passing the random email to the test_create_user fixture
    mobile = "+" + fake.phone_number()
    name = fake.name()
    first_name, last_name = name.split()
    date = fake.date()
    year, month, day = date.split("-")
    title = random.choice(valid_titles)
    payload = {
               "name": name,
               "email": fake.email(),
               "password": fake.password(),
               "title": title,
               "birth_date": day,
               "birth_month": month,
               "birth_year": year,
               "firstname": first_name,
               "lastname": last_name,
               "company": fake.company(),
               "address1": fake.address(),
               "address2": fake.address(),
               "country": fake.country(),
               "zipcode": fake.zipcode(),
               "state": fake.state(),
               "city": fake.city(),
               "mobile_number": mobile,
               }
    requests.post(ENDPOINT + "/createAccount", data=payload)
    return payload["email"], payload["password"]

@pytest.fixture
def test_can_post_to_delete_user_account(test_create_user): ## test_create_user fixture is returning the random email
     email, password = test_create_user
     payload = {
               "email": email,
               "password": password,
               }
     requests.delete(ENDPOINT + "/deleteAccount", data=payload) ## Deleting the user with the generated email
     yield test_create_user ## Stoping the fixture executing and return the random email back to the test function


def test_user_not_exist(test_can_post_to_delete_user_account, test_create_user):

    email_of_created_user, password_of_created_user = test_create_user ## I took the email of created person, and took the same email after deletion flow, and compare them, because
                                                                       ## this test will show expected 404 error, EVEN when email is not the same. But i want to know, that the EXACT person was deleted.
    email, password = test_can_post_to_delete_user_account

    payload = {
               "email": email,
               "password": password
               }
    response = requests.post(ENDPOINT + "/verifyLogin", data=payload)
    data = response.json()
    assert data["responseCode"] == 404
    assert data["message"] == "User not found!"
    assert email_of_created_user == email, "It's not the same person!"
    assert password_of_created_user == password, "It's not the same person!"

## --------------- API 13: PUT METHOD To Update User Account/API 14: GET user account detail by email  ---------------

@pytest.fixture
def test_create_user_for_update(valid_titles): ## Passing the random email to the test_create_user fixture
    mobile = "+" + fake.phone_number()
    name = fake.name()
    first_name, last_name = name.split()
    date = fake.date()
    year, month, day = date.split("-")
    title = random.choice(valid_titles)
    payload = {
               "name": name,
               "email": fake.email(),
               "password": fake.password(),
               "title": title,
               "birth_date": day,
               "birth_month": month,
               "birth_year": year,
               "firstname": first_name,
               "lastname": last_name,
               "company": fake.company(),
               "address1": fake.address(),
               "address2": fake.address(),
               "country": fake.country(),
               "zipcode": fake.zipcode(),
               "state": fake.state(),
               "city": fake.city(),
               "mobile_number": mobile,
               }
    requests.post(ENDPOINT + "/createAccount", data=payload)
    return payload

@pytest.fixture
def test_update_user(test_create_user_for_update, valid_titles):

    mobile = "+" + fake.phone_number()
    name = fake.name()
    first_name, last_name = name.split()
    date = fake.date()
    year, month, day = date.split("-")
    title = random.choice(valid_titles)
    payload = {
               "name": name,
               "email": test_create_user_for_update["email"],
               "password": test_create_user_for_update["password"],
               "title": title,
               "birth_date": day,
               "birth_month": month,
               "birth_year": year,
               "firstname": first_name,
               "lastname": last_name,
               "company": fake.company(),
               "address1": fake.address(),
               "address2": fake.address(),
               "country": fake.country(),
               "zipcode": fake.zipcode(),
               "state": fake.state(),
               "city": fake.city(),
               "mobile_number": mobile,
               }
    requests.put(ENDPOINT + "/updateAccount", data=payload)
    return payload

def test_updated_user(test_update_user):
    payload = {"email": test_update_user["email"]}
    response = requests.get(ENDPOINT + "/getUserDetailByEmail", params=payload)
    data = response.json()
    user_data = data["user"]
    assert data["responseCode"] == 200
    assert user_data["name"] == test_update_user["name"]
    assert user_data["email"] == test_update_user["email"]
    # assert user_data["password"] == test_update_user["password"] this field is not returned. Expected))))
    assert user_data["title"] == test_update_user["title"]
    assert user_data["birth_day"] == test_update_user["birth_date"] ## WTH??? bug. Keys name are different
    assert user_data["birth_month"] == test_update_user["birth_month"]
    assert user_data["birth_year"] == test_update_user["birth_year"]
    assert user_data["first_name"] == test_update_user["firstname"]
    assert user_data["last_name"] == test_update_user["lastname"]
    assert user_data["company"] == test_update_user["company"]
    assert user_data["address1"] == test_update_user["address1"]
    assert user_data["address2"] == test_update_user["address2"]
    assert user_data["country"] == test_update_user["country"]
    assert user_data["zipcode"] == test_update_user["zipcode"]
    assert user_data["state"] == test_update_user["state"]
    assert user_data["city"] == test_update_user["city"]
    # assert user_data["mobile_number"] == test_update_user["mobile_number"] where is mobile??? lol. Get request doesn't returned the mobile
