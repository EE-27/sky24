import requests
import stripe

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

pr = Product("Testblabla",9999999)
def payment_create():
    stripe.api_key = "sk_test_51OeCgjBVY8RAQhG3hJ8Hs8PraP29hbB8lBal33CM3OYWMKkkNXW9dcVHaMtxGmOy4FvZiDwy1ahbbPytfQcSVWsf007kbIKswV"

    # Create a Product on Stripe
    product_data = {
        'name': f'{pr.name}',
        "type" : "service"}


    response = requests.post('https://api.stripe.com/v1/products', data=product_data,
                             headers={'Authorization': f'Bearer {stripe.api_key}'})

    product = response.json()
    product_response = response.json()
    print(product_response)

    # Retrieve the product ID from the response
    product_id = product_response.get('id')

    # Create a Price for the Product
    price_data = {
        'product': product_id,
        'unit_amount': f'{pr.price}',
        'currency': 'czk',
    }
    response = requests.post('https://api.stripe.com/v1/prices', data=price_data,
                             headers={'Authorization': f'Bearer {stripe.api_key}'})

    price = response.json()
    price_response = response.json()
    price_id = price_response.get("id")
    print(price_response)
    # Create a PaymentLink
    payment_link_data = {
        'line_items': [{'price': price_id, 'quantity': 1}]
    }
    payment_link_response = stripe.PaymentLink.create(**payment_link_data)
    print(payment_link_response["url"])

payment_create()