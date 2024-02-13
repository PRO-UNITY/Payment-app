import stripe

stripe.api_key = "sk_test_51OirCFLZ26NOlTGBlprWJXdfakpoZ8Y6cnS8t2eq7sumT26UT5SDt5qW99j5oZEIxhkTBcomG8HfAbR5h2Ye7hND00xsAUxZxV"

# stripe.api_key = "pk_test_51OirCFLZ26NOlTGBPqA4VQbX9UNih1vM8cJfm0xNohLNjMEEc2w3vxJjJdsFc0fSlfczmxGKFizW0H1rB0Dea2Jp00Flw7XUUR"

customer_id = "cus_PY5l9kRzh0CvVI"
token = "tok_1OiwwGLZ26NOlTGBe3BQdVAX"



# intent = stripe.Charge.create(
#     amount=200,
#     currency='usd',
#     source=token,
#     description='Example charge'
# )

# def create_customer(email, card_token):
#     try:
#         # Create a customer with the email
#         customer = stripe.Customer.create(email=email)

#         # Attach the card to the customer
#         stripe.Customer.create_source(customer.id, source=card_token)

#         return customer.id
#     except stripe.error.StripeError as e:
#         # Handle Stripe errors
#         print("Stripe error:", str(e))
#         return None

# # Example usage:
# email = "example@example.com"
# card_token = "tok_1OiyqDLZ26NOlTGBCmLtXbUM"  # Replace with the actual card token
# customer_id = create_customer(email, card_token)
# if customer_id:
#     print("Customer created successfully with ID:", customer_id)
# else:
#     print("Failed to create customer")

# try:
#     card = stripe.Customer.create_source(
#         customer_id,
#         source=card_token
#     )
#     print(card)
# except stripe.error.CardError as e:
#     # Handle card errors
#     pass
# except stripe.error.StripeError as e:
#     # Handle other Stripe errors
#     pass
# except Exception as e:
#     # Handle other exceptions
#     pass
# print(intent)



# def get_customer_cards(customer_id):
#     try:
#         # Retrieve customer's sources (cards)
#         cards = stripe.Customer.list_sources(
#             customer_id,
#             object='card'
#         )
#         return cards.data
#     except stripe.error.StripeError as e:
#         # Handle Stripe errors
#         print("Stripe error:", str(e))
#         return None

# # Example usage:
# customer_id = "cus_PY5l9kRzh0CvVI"  # Replace with the actual customer ID
# cards = get_customer_cards(customer_id)
# if cards:
#     print("Customer cards:")
#     for card in cards:
#         print("Card ID:", card.id)
#         print("Brand:", card.brand)
#         print("Last 4 digits:", card.last4)
#         print("Expiry month:", card.exp_month)
#         print("Expiry year:", card.exp_year)
#         print("--------------------")
# else:
#     print("Failed to retrieve customer cards")



# def get_customer_balance(customer_id):
#     try:
#         # Retrieve the customer object from Stripe
#         customer = stripe.Customer.retrieve(customer_id)
        
#         # Access the balance attribute of the customer object
#         balance = customer.balance
#         return balance
#     except stripe.error.StripeError as e:
#         # Handle Stripe errors
#         print("Stripe error:", str(e))
#         return None

# # Example usage:
# customer_id = "cus_PY5l9kRzh0CvVI"  # Replace with the actual customer ID
# balance = get_customer_balance(customer_id)
# if balance is not None:
#     print("Customer balance:", balance)
# else:
#     print("Failed to retrieve customer balance")



def process_payment(customer_id, card_id, amount, currency='usd'):
    try:
        # Create a charge using the customer ID and card ID
        stripe.api_key = "sk_test_51OirCFLZ26NOlTGBlprWJXdfakpoZ8Y6cnS8t2eq7sumT26UT5SDt5qW99j5oZEIxhkTBcomG8HfAbR5h2Ye7hND00xsAUxZxV"

        charge = stripe.Charge.create(
            amount=amount,  # Amount in cents
            currency=currency,
            customer=customer_id,
            source=card_id,  # ID of the saved card
            description='Payment for your order'
        )
        return charge
    except stripe.error.StripeError as e:
        # Handle Stripe errors
        print("Stripe error:", str(e))
        return None

# Example usage:
customer_id = "cus_PY8hmuRWHRdNnP"  # Replace with the actual customer ID
card_id = "card_1Oj2OgLZ26NOlTGBL9upszXm"  # Replace with the actual card ID
amount = 2222  # Amount in cents ($10.00)
currency = 'usd'

charge = process_payment(customer_id, card_id, amount, currency)
if charge:
    print("Payment successful! Charge ID:", charge.id)
else:
    print("Payment failed.")