import stripe
stripe.api_key = "sk_test_51OeCgjBVY8RAQhG3hJ8Hs8PraP29hbB8lBal33CM3OYWMKkkNXW9dcVHaMtxGmOy4FvZiDwy1ahbbPytfQcSVWsf007kbIKswV"

def ppl():
    product = stripe.Product.create(
      name="Starter Setup",
      default_price_data={"unit_amount": 2000, "currency": "usd"},
      expand=["default_price"],
    )


    price = stripe.Price.create(
      product=product,
      unit_amount=99999,
      currency="czk",
    )

    x = stripe.PaymentLink.create(
      line_items=[{"price": price, "quantity": 1}],
    )
    print(x.id)
    print(x["url"])
    payment_intent = stripe.PaymentIntent.create(
        amount=987,
        currency='usd',
        metadata={"payment_link_id": x.id}  # Associate the PaymentLink ID with the PaymentIntent
    )
    return payment_intent

# payment_intent = ppl()
#
# payment_id = payment_intent.get('id')
# print(payment_intent.get('id'))
payment_id = "pi_3Oea3FBVY8RAQhG31LHKAlvr"
payment_retrive = stripe.PaymentIntent.retrieve(payment_id)
print(payment_retrive)
# # print({'status': payment_intent.status , 'body': payment_intent})


"""
plink_1Oea3FBVY8RAQhG3xzqSPjUq
https://buy.stripe.com/test_7sIdRy9mdcHq5PO3dG
pi_3Oea3FBVY8RAQhG31LHKAlvr
"""