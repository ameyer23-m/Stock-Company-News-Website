"""
This code creates a dataset that contains information on news articles and tweets about the companies, 
including the company name, article name, date, publisher, writer.
"""

import random
import datetime
import csv

# Define company names, publishers, and writers
companies = ["Apex Corporation","Maritime Data","Fusion Energy","Bitterroot Wood Studio","Echo"]
publishers = ['New York Times', 'Washington Post', 'Wall Street Journal', 'USA Today', 'Los Angeles Times','ABC News', 'BBC News', 'CNN', 'Fox News', 'NBC News', 'The Boston Globe', 'Time Magazine', 'Politico', 'Bloomberg News', 'NPR']
writers = ['Milo Wilson', 'Remy Thompson', 'Jade Parker', 'Camryn Baker', 'Skyler Green', 'Quincy Brooks', 'Avery Martin', 'Rory Evans', 'Lennon Hill', 'Phoenix Scott', 'Rowan Reed', 'Noel Clarke', 'Emory Fisher', 'Harley Nelson', 'Elliot Morgan', 'Finley Mitchell', 'August Sanchez', 'Sawyer Baker', 'Charlie Taylor', 'Ashton Diaz', 'Toby Reyes', 'Blake Hughes', 'Dakota Young', 'Logan Coleman', 'Parker Wright']

# Define start and end dates
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2023, 8, 4)

# Create list
data = []

# create a list of all the dates between start and end date
all_dates = [start_date + datetime.timedelta(days=x) for x in range((end_date - start_date).days + 1)]


for company in companies:
    # selects 15 dates randomly
    random.shuffle(all_dates)
    selected_dates = all_dates[:15]
    selected_dates.sort()

    for date in selected_dates:
        # adds row to be modified later
        article_name = f""
        # adds randomly selected info
        date = date
        publisher = random.choice(publishers)
        writer = random.choice(writers)
        
#         # Append data to the list
        data.append([company, article_name, date.strftime('%m/%d/%Y'), publisher, writer])
    
# Add to csv
with open('company_news.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Company Name', 'Article Name', 'Date', 'Publisher', 'Writer'])
    writer.writerows(data)
    