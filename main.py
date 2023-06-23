import json
from tkinter import *
import requests
import csv
import tkinter.font as tkFont

# Create the Tkinter window
screen = Tk()
screen.title("Currency Converter App")
screen.geometry("500x800")

# Setting icon of window
icon = PhotoImage(file='icon.png')
screen.iconphoto(True, icon)

# Function to handle button click and perform currency conversion
def results():
    global from_currency_iso
    
    # Get the selected "from" currency code
    from_currency_name = from_currency.get()
    if from_currency_name in CurrencyName:
        index = CurrencyName.index(from_currency_name)
        from_currency_iso = CurrencyCode[index]
    
    # Get the selected "to" currency code
    to_currency_name = to_currency.get()
    if to_currency_name in CurrencyName:
        index = CurrencyName.index(to_currency_name)
        to_currency_iso = CurrencyCode[index]
    
    # Check if the user entered a valid amount
    try:
        global amount
        amount = float(entered_amount.get())
    except ValueError:
        var_results.set("ERROR")
        return
    
    # Make API request to get the conversion rate
    response = requests.get(f"https://api.exchangerate.host/convert?amount={amount}&from={from_currency_iso}&to={to_currency_iso}")
    api_results = response.json()['result']
    
    # Remove unnecessary characters from the result
    remove_chars = "{ } ' ' a b c d  f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z : "
    for char in remove_chars:
        api_results = str(api_results).replace(char, "")
    
    # Format the result with decimal places
    if float(api_results) > 9999999999:
        var_results.set("Too Long")
        return
    elif not float(api_results) < 0.01:
        api_results = '%.2f' % float(api_results)
    elif not float(api_results) < 0.001:
        api_results = '%.3f' % float(api_results)
    elif not float(api_results) < 0.0001:
        api_results = '%.4f' % float(api_results)
    elif not float(api_results) < 0.00001:
        api_results = '%.5f' % float(api_results)
    elif not float(api_results) < 0.000001:
        api_results = '%.6f' % float(api_results)
    else:
        var_results.set("Too Long")
        return
    
    var_results.set(api_results + " " + to_currency_iso)

# Read currency data from the CSV file
csv_file = open('currencies.csv', 'r')
file = csv.DictReader(csv_file)
CurrencyName = []
CurrencyCode = []
for col in file:
    CurrencyCode.append(col['CurrencyCode'])
    CurrencyName.append(col['CurrencyName'])

# Font size for the dropdown menu
drop_font = tkFont.Font(family="Verdana", size=15)

# GUI elements
Label(screen, text="Currency Conversion", font=("Courier", 35)).pack(pady=20)
from_text = Label(screen, text="From:", font=(None, 25))
from_text.pack(pady=20, padx=75, anchor="w")

from_currency = StringVar()
from_currency.set(CurrencyName[142])  # Default currency: USD
from_drop = OptionMenu(screen, from_currency, *CurrencyName)
from_drop.pack(padx=75, anchor="w")
from_drop.config(font=drop_font)

from_text = Label(screen, text="To:", font=(None, 25))
from_text.pack(pady=20, padx=75, anchor="w")

to_currency = StringVar()
to_currency.set(CurrencyName[46])  # Default currency: GBP
to_drop = OptionMenu(screen, to_currency, *CurrencyName)
to_drop.pack(padx=75, anchor="w")
to_drop.config(font=drop_font)

entered_amount = StringVar()
entered_amount.set("1")

amount_text = Label(screen, text="Amount:", font=(None, 25))
amount_text.pack(pady=20, padx=75, anchor="w")

amount_data = Entry(screen, textvariable=entered_amount)
amount_data.pack(padx=75, anchor="w")

Button(screen, text="Convert", command=results).pack(pady=30, padx=75, anchor="w")

var_results = StringVar()
var_results.set("Results")
results_label = Label(screen, textvariable=var_results, borderwidth=7, font=("Currency", 30), relief="solid", width=14,height=3, bg="#FFD733").pack(pady=20, padx=75, anchor="w")

screen.mainloop()
