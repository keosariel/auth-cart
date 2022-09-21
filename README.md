#### Response Data

| field   | description                                            |
| ------- | ------------------------------------------------------ |
| code    | API status code i.e E104                               |
| status  | HTTPS status code 200                                  |
| message | Insights on the current `code` is there was an error |
| data    | request data                                          |

#### Field Validation

| field    | regex                                                             |
| -------- | ----------------------------------------------------------------- |
| name     | ^[a-zA-Z]{2,15}$                                                  |
| username | ^[a-z0-9_]{3,15}$                                                 |
| email    | [^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+                           |
| password | ^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$ |

#### Signup

**Route**: `/auth/signup`

**Method**: `POST`

**Headers** `Authorization`

| Fields    | type                    | required |
| --------- | ----------------------- | -------- |
| firstname | string (name-regex)     | required |
| lastname  | string (name-regex)     | required |
| username  | string (username-regex) | required |
| email     | string (email-regex)    | required |
| password  | string (password-regex) | required |

---

#### Login

**Route**: `/auth/login`

**Method**: `POST`

**Headers** `Authorization`

| Fields   | type   | required |
| -------- | ------ | -------- |
| email    | string | required |
| password | string | required |

---

#### Create carts for new session

**Route**: `/carts`

**Method**: `POST`

**Headers** `Authorization`

---

#### Add item to cart

**Route**: `/carts/<string:cart_public_id>`

**Method**: `POST`

**Headers** `Authorization`

| Fields  | type   | required |
| ------- | ------ | -------- |
| item_id | string | required |

#### Delete cart item

**Route**: `/carts/<`string:cart_public_id `>`

**Method**: `Delete`

**Headers** `Authorization`

| Fields  | type   | required |
| ------- | ------ | -------- |
| item_id | string | required |

---

#### Get User Checkedout Cart

In situations where a user has paid for cart items, a checkout `post` request should be made to the carts id `cart_public_id` i.e POST => ``/carts/checkedout/[string:cart_public_id](string:cart_public_id) .``

This request gets checkedout carts, in other words carts that has been paid for.

**Route**: `/carts/checkedout`

**Method**: `GET`

**Headers** `Authorization`

---

#### Checkout a Cart

**Route**: `/carts/checkedout/<string:cart_public_id>`

**Method**: `POST`

**Headers** `Authorization`
