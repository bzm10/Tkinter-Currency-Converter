import requests

print("\nEnter Currency Symbol e.g. (USD, EUR, GBP)\n")

from_currency = input("Enter the currency to convert from: ")
to_currency = input("Enter the currency to convert to: ")
amount = float(input("Enter the amount: "))

# Get the data from the API
response = requests.get(f"https://api.exchangerate.host/convert?amount={amount}&from={from_currency}&to={to_currency}")

# Print the result
if response.json()['result'] is None:
    print('ERROR: One or both of the entered symbols are invalid.')
else:
    print(response.json()['result'])
