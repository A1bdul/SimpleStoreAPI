# Simple Store

Simple estore rest api 
 
# Requirements 

    Django, Python
    Django-rest-framework
    Uploadcare

# Installation

Run the following commands from your shell, 
Python version>=3.8 should be installed 

Project cloning and dependent package installation:

    git clone https://github.com/A1bdul/SimpleStore
    cd ChatApp
    pip install -r requirements.txt
    
Defining all hidden credentials in your .env file. Your uploadcare public and secret key
 is available in the 
dashboard of your uploadcare account.
Creating a local database and running a web server:

    python manage.py migrate --run-syncdb
    python manage.py runserver


Create admin user to login into website and control dashboard
    python manage.py createsuperuser
    

You can now browse the following [link](http://localhost:8000)

    http://localhost:800/

Add new product to page.


# End Points

## api/product 

    GET, POST request Only
    full list of product that have atleast one item avaiable
    

## api/user
    GET, POST request Only
    --GET
        authenticated user wish list and and cart from database
    --POST
        add and remove from user wish list, 
        send product id in request, product is added or removed based on 
        whether item is available in user's wish list


## api/cart
    POST request Only
    add and remove from user cart
    send product id in request, product is added or removed based on 
    whether item is available in user's cart

## api/checkout-point
    POST request Only
    verify contacts, confirm payemnt and start shipping processing
    authenticated user cart is taken from database, non-authenticated user send in cart, 
    both send in address form with request
        shipping_address: {
                    firstname: firstname,
                    lastname: lastname,
                    email: email,
                    mobile_number: mobile_number,
                    zip: zip,
                    city: city,
                    address: address
                },
                cart: {
                    "items": [{
                        "item": {
                            "name": "Laced Jacket With Strips",
                            "id": 2
                        }, "quantity": 1
                    }, ]
        }
    can validate the shipping address and send success or error response back,
    if gateway payment system confirms payemnt, sending post request, 
        {payment: 'confirmed'}
    end point changes cart status to processing and send email to user email, owner 
    email to confirm and start delivery

