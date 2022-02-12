from flask_jsonvalidator import (
    JSONValidator,
    StringValidator,
    IntValidator,
    BooleanValidator,
    ArrayOfValidator
)

Name = "^[a-zA-Z]{2,15}$"
USERNAME = "^[a-z0-9_]{3,15}$"
EMAIL    = "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"
PASSWORD = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$"

class LoginValidator(JSONValidator):
    validators = {
        "email"  : StringValidator(nullable=False),
        "password" : StringValidator(nullable=False),
    }

class SignupValidator(JSONValidator):
    validators = {
        "firstname"  : StringValidator(regex=Name, nullable=False),
        "lastname"  : StringValidator(regex=Name, nullable=False),
        "username"  : StringValidator(regex=USERNAME, nullable=False),
        "email"  : StringValidator(regex=EMAIL, nullable=False),
        "password" : StringValidator(nullable=False)
    }

class CartItemValidator(JSONValidator):
    validators = {
        "item_id" : StringValidator(nullable=False)
    }