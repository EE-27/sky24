# pip3 install stripe

import stripe
stripe.api_key = "sk_test_51OeCgjBVY8RAQhG3hJ8Hs8PraP29hbB8lBal33CM3OYWMKkkNXW9dcVHaMtxGmOy4FvZiDwy1ahbbPytfQcSVWsf007kbIKswV"

product = stripe.Product.create(
  name="Starter Setup",
  default_price_data={"unit_amount": 2000, "currency": "usd"},
  expand=["default_price"],
)


price = stripe.Price.create(
  product=product,
  unit_amount=14587,
  currency="czk",
  recurring={"interval": "month"},
)

x = stripe.PaymentLink.create(
  line_items=[{"price": price, "quantity": 1}],
)
print(x.id)
print(x["url"])

###
#
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import stripe
# from .serializers import CourseSerializer  # Make sure to import your serializer
#
#
# class CoursePaymentCreateAPIView(APIView):
#   serializer_class = CourseSerializer
#
#   def post(self, request):
#     stripe.api_key = "sk_test_51OeCgjBVY8RAQhG3hJ8Hs8PraP29hbB8lBal33CM3OYWMKkkNXW9dcVHaMtxGmOy4FvZiDwy1ahbbPytfQcSVWsf007kbIKswV"
#
#     try:
#       # Create a Product
#       product = stripe.Product.create(
#         name="Starter Setup",
#         type="service"  # or "good" depending on your use case
#       )
#
#       # Create a Price for the Product
#       price = stripe.Price.create(
#         product=product.id,
#         unit_amount=2000,
#         currency="usd",
#       )
#
#       # Create a PaymentLink
#       payment_link = stripe.PaymentLink.create(
#         line_items=[{"price": price.id, "quantity": 1}],
#         success_url="http://localhost:8000/courses/payment-success",  # Replace with your success URL
#         cancel_url="http://localhost:8000/courses/payment-cancel",  # Replace with your cancel URL
#       )
#
#       # Return the payment link URL
#       return Response({'payment_link_url': payment_link.url}, status=status.HTTP_200_OK)
#
#     except stripe.error.StripeError as e:
#       # Handle Stripe errors
#       return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# import requests
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import CourseSerializer  # Make sure to import your serializer
#
#
# class CoursePaymentCreateAPIView(APIView):
#   serializer_class = CourseSerializer
#
#   def post(self, request):
#     stripe.api_key = "sk_test_51OeCgjBVY8RAQhG3hJ8Hs8PraP29hbB8lBal33CM3OYWMKkkNXW9dcVHaMtxGmOy4FvZiDwy1ahbbPytfQcSVWsf007kbIKswV"
#
#     try:
#       # Create a Product on Stripe
#       product_data = {
#         'name': 'Starter Setup',  # Adjust the name as needed
#         'default_price_data': {'unit_amount': 2000, 'currency': 'usd'},
#         'expand': ['default_price'],
#       }
#       response = requests.post('https://api.stripe.com/v1/products/', data=product_data,
#                                headers={'Authorization': f'Bearer {stripe.api_key}'})
#
#       # Check if the product creation was successful
#       if response.status_code != 200:
#         return Response({'error': f'Failed to create product on Stripe: {response.text}'}, status=response.status_code)
#
#       product = response.json()
#
#       # Create a Price for the Product
#       price_data = {
#         'product': product['id'],
#         'unit_amount': 2000,
#         'currency': 'usd',
#         'recurring': {'interval': 'month'},
#       }
#       response = requests.post('https://api.stripe.com/v1/prices/', data=price_data,
#                                headers={'Authorization': f'Bearer {stripe.api_key}'})
#
#       # Check if the price creation was successful
#       if response.status_code != 200:
#         return Response({'error': f'Failed to create price on Stripe: {response.text}'}, status=response.status_code)
#
#       price = response.json()
#
#       # Create a PaymentLink
#       payment_link_data = {
#         'line_items': [{'price': price['id'], 'quantity': 1}]
#       }
#       payment_link_response = stripe.PaymentLink.create(**payment_link_data)
#
#       return Response({'payment_link_url': payment_link_response.url}, status=status.HTTP_200_OK)
#
#     except stripe.error.StripeError as e:
#       # Handle Stripe errors
#       return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
