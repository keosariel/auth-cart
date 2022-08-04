import requests
import json

# create account
data = {
    "firstname" : "kenneth",
    "lastname"  : "gabriel",
    "username"  : "keosariel",
    "email"     : "kennethgabriel78@gmail.com",
    "password"  : "password78"
}

res = requests.post("http://127.0.0.1:5000/auth/signup", json=data)

print(res.text)

res = requests.post("http://127.0.0.1:5000/auth/login", json=data)

print(res.text)

user = json.loads(res.text)

res = requests.post("http://127.0.0.1:5000/carts", headers={"Authorization":"Bearer "+user.get("token")})

print(res.text)

cart = json.loads(res.text)

res = requests.put(f"http://127.0.0.1:5000/carts/{cart.get('id')}", json={"item_id":"video_id"}, headers={"Authorization":"Bearer "+user.get("token")})

print(res.text)

cart_item = json.loads(res.text)


res = requests.get(f"http://127.0.0.1:5000/carts/{cart.get('id')}", headers={"Authorization":"Bearer "+user.get("token")})

print(res.text)

cart = json.loads(res.text)
