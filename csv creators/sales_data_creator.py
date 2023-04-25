"""
This code creates the company sales needed for the base of our dataset with the following variables:
company name, order id, order date, ship date, shipping type, product, sales, profit, shipping cost, year

Created by Adam Meyer
"""

import random
import datetime
import csv
import uuid

# Define company names and their products
companies = {
    "Apex Corporation": ["accessories", "phones", "computers", "tablets", "televisions"],
    "Maritime Data": ["Cloud Service", "Banking platform", "Business Analytics", "Database Security", "GPU Software", "Workforce Scheduling"],
    "Fusion Energy": ["Combustion Fluids", "Cleaning Supplies", "Greases", "Rubber"],
    "Bitterroot Wood Studio": ["Chairs", "Tables", "Bedframes", "Bookcases", "Cabinets"],
    "Echo": ["accessories", "phones", "computers", "tablets", "washers", "dryers", "car radios"]
}


# Define start and end dates
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2023, 8, 4)

shipping_types = ["Standard", "Express", "Same Day"]

# Create list
data = []

# Create a set to keep track of used order IDs
used_order_ids = set()

# Create a loop for each order
while start_date <= end_date:
    for company, products in companies.items():
        for product in products:
             # Generate a unique order ID
            while True:
                order_id = str(uuid.uuid4())[:3] + '-' + str(uuid.uuid4())[4:8]
                if order_id not in used_order_ids:
                    used_order_ids.add(order_id)
                    break

            order_date = start_date
            shipping_type = random.choice(list(shipping_types))
                # Determine the shipping date
            if shipping_type == "Same Day":
                ship_date = order_date
            elif shipping_type == "Express":
                # Express Shipping
                ship_date = order_date + datetime.timedelta(days=2)
            else:
                # Standard Shipping, but cant ship on sundays
                ship_date = order_date + datetime.timedelta(days=random.choice(range(4, 8)))
                if ship_date.weekday() == 6:
                    ship_date += datetime.timedelta(days=1)
            
            sales = random.randint(10, 300)
            profit = round(random.uniform(20, 300), 2)
            shipping_cost = round(random.uniform(10, 100), 2)
            year = order_date.year
            
            # Append data to the list
            data.append([company, order_id, order_date.strftime('%m/%d/%Y'), ship_date.strftime('%m/%d/%Y'), shipping_type, product, sales, profit, shipping_cost, year])

    # Increment the start date by a random number of days (1-3 days)
    start_date += datetime.timedelta(days=random.randint(1, 3))

# Add to csv
with open('product_sales.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['company_name', 'order_id', 'order_date', 'ship_date', 'shipping_type', 'product', 'sales', 'profit', 'shipping_cost', 'year'])
    writer.writerows(data)
    