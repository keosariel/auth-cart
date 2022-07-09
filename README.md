#### Field Validation

field | regex
------|------
name | ^[a-zA-Z]{2,15}$
username | ^[a-z0-9_]{3,15}$
email | [^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+
password | ^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$

#### Signup

**Route**: `/auth/signp`

**Method**: `POST`

**Headers** `Authorization`

Fields | type | required
-------|------|---------
firstname | string (name-regex) | required
lastname | string (name-regex) | required
username | string (username-regex) | required
email | string (email-regex) | required
password | string (password-regex) | required

-----

#### Login

**Route**: `/auth/signp`

**Method**: `POST`

**Headers** `Authorization`

Fields | type | required
-------|------|---------
email | string | required
password | string | required

-----

#### Create carts

**Route**: `/carts`

**Method**: `POST`

**Headers** `Authorization`

-----

#### Add item to cart

**Route**: `/carts/<string:public_id>`

**Method**: `POST`

**Headers** `Authorization`

Fields | type | required
-------|------|---------
item_id | string | required

-----

#### Get User Checkedout Cart

**Route**: `/carts/checkedout`

**Method**: `GET`

**Headers** `Authorization`

-----

#### Checkout Cart

**Route**: `/carts/checkedout/<string:public_id>`

**Method**: `POST`

**Headers** `Authorization`

Fields | type | required
-------|------|---------
item_id | string | required
