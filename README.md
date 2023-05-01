# Invest Insights

## Description
A website that allows any visitor to see news stories and information a certain stock companies, while along being able to create their own profile for the website.

## How To Setup Enviroment
To run this program you first want to clone the repository from GitHub, then you create a virtual environment using `python -m venv ./venv` or `python3 -m venv ./venv`. Then to activate the enviorment run `venv\Scripts\activate` for windows or `source ./venv/bin/activate` for MacOS. Once your enviroment is active, install the requirments using `pip install -r requirements.txt`. Now that your first time setup is done, you are ready to run the program. The to run, the first step is to make sure you are still in your virtual enviroment. For me I have to set `FLASK_APP=app\main_app.py` in the terminal. Next, you will want to run `flask initdb`. This will setup your database and destroy anything inside of it. Now all you have to do is `flask run` and the program is running.

# More Updates to come...
