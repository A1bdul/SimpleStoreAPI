# Simple Store

Simple estore rest api 
 
# Requirements 

    Django, Python
    Django-rest-framework
    Uploadcare

# Installation

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

