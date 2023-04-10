"""
This code creates the fake stock price needed for the base of our dataset with the following variables:
stock abbreviation, date, opening price, daily max price, daily min price, closing price

Created by Adam Meyer
"""

import csv
import datetime
import random

# create stock name
stocks = ["APX", "MTD", "FEN", "BWS", "ECH"]

# Create list
data = []

# Get data for each stock
for stock in stocks:

    # Define start and end dates
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2023, 8, 4)

    # Set opening price for each stock
    if stock == "APX":
        opening_price = 165.65
    elif stock == "MTD":
        opening_price = 53.95
    elif stock == "FEN":
        opening_price = 70.33
    elif stock == "BWS":
        opening_price = 20.19
    elif stock == "ECH":
        opening_price = 39.64
    else:
        print("This is not an actual stock name!")

    # Create a loop for each day
    current_date = start_date
    while current_date <= end_date:

        # Check if current date is a weekday
        if current_date.weekday() < 5:

            stock_abbrev = stock
            if datetime.date(2020, 3, 19) <= current_date <= datetime.date(2020, 5, 4):
                daily_max = round(random.uniform(opening_price, opening_price * 1.2), 2)
                daily_min = round(random.uniform(opening_price * 0.7, opening_price), 2)
            else:
                daily_max = round(random.uniform(opening_price, opening_price * 1.1000001), 2)
                daily_min = round(random.uniform(opening_price * 0.9, opening_price), 2)
            closing_price = round(random.uniform(daily_min, daily_max), 2)
            data.append([stock_abbrev, current_date.strftime('%m/%d/%Y'), opening_price, daily_max, daily_min, closing_price])
            opening_price = closing_price
    
        current_date += datetime.timedelta(days=1)

# Add to csv
with open('stock_prices.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['stock_abbrev', 'date', 'opening_price', 'daily_max', 'daily_min', 'closing_price'])
    writer.writerows(data)
