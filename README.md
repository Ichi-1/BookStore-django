## Demo: [BookStore](https://ichi1-bookstore.herokuapp.com/)

### Tech-Stack:
- Web-framework: Django 4.0.5
- RDBMS: PostgreSQL
- Cloud storage: Cloudinary 
- Styling: Boostrap 4

### User data for testing
<details>
  <summary>User Account Credentials</summary>
  
  ```
  Username: jid59797@xcoxc.com
  Password: bSUfVRmeUe3k8Bd
  ```
  
</details>

<details>
  <summary>PayPal SandBox credential</summary>
  
  Chech this docs file. Let me know if sandbox money account was exousted 
  ```
  /docs/paypal.txt
  ```
</details>


### Aims of this project
When i start working on this project my main goal was an implement a full-cycle of ecommerce user experience. To achive that goal i create a few modular, which must provide for regular user ability to manage his personal data, whishlist and order list. One of the key features of this project is session-based basket(apps/basket/basket.py) and Multi-Product Types DB, which is easys to scale up and can be used for any kind of e-commerce assortment. 
You can check db relations schemas via docs/store_db_schema.txt (fit to https://dbdiagram.io/, in example):
```
Table Product as P {
  id int [pk, increment]
  product_type int
  category int
  description varchar
  slug slug
  regular_price decimal
  discount_price decimal
  is_active boolean
  created_at timestamp
  updated_at timestamp
}
Ref: PT.id < P.product_type 
Ref: C.id < P.category
```

### Full-cycle of user experience if this app consist of next stages:
- Signing Up and activate account from email link (SMTP configuratet for that)
- Navigate throught the application with navbar, 
  - viewing personal dashboard and manage account data  
  - viewing store catalogue via categories of products
- User can learn more about specific product via DetailView, that provide product specification (assortment)
- Adding wanted product to whishlist or to basket
- Proceed to checkout and pay
- After payment - track billing orders in special account section 

### Configuration 
```
python3 -m venv venv
. venv/bin/activate
pip install -r requriments
```
Also you need to provide your own .evn variables for SMTP, django app, cloud storage and PayPal.
Getting secret key via django utils:
```
python3 manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```


#### TODO List:
- ~~PostgreSQL conf for prod~~
- ~~Real-world SMTP and mail activation service~~
- Email notification after billing
- Rating\Reviews system
- Live Support Chat (Django Channels)
  - Maybe i will start chat app as isolated, autonomous service and when it will be ready - link it with main e-commerce as microservice
- Searching bar and filters 
- Refactoring ProductDetailView. DRY
- Login & Security Options (2fa)
- 'Read More' btn in Detail Template

