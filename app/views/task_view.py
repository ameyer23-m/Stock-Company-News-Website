from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint, redirect, make_response
# from models.task import Task, TaskDB
# from models.companies_modifier import Company, CompanyDB
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm


from models.users_modifier import User, UserDB
from models.companies_modifier import Company, CompanyDB

task_list_blueprint = Blueprint('task_list_blueprint', __name__)

IS_LOGGED_IN = False;

news = [
    {
        'company': 'APX',
        'article': 'Article 1 on APX with a super long title that I dont like',
        'date': '2022-01-03',
        'publisher': 'NY Times',
        'writer': 'Joe Biden'
    },
    {
        'company': 'APX',
        'article': 'Article 2 on APX',
        'date': '2022-01-04',
        'publisher': 'NY Times',
        'writer': 'Joe Biden'
    },
    {
        'company': 'MTD',
        'article': 'Article 1 on MTD ',
        'date': '2022-01-04',
        'publisher': 'Time Magazine',
        'writer': 'Susan Test'
    },
    {
        'company': 'MSFT',
        'article': 'Article 2 on ECH ',
        'date': '2022-01-10',
        'publisher': 'Time Magazine',
        'writer': 'Susan Test'
    },
    {
        'company': 'MSFT',
        'article': 'Article 3 on ECH ',
        'date': '2022-04-04',
        'publisher': 'NBC',
        'writer': 'Jon Snow'
    },
    {
        'company': 'BWS',
        'article': 'Article 1 on BWS ',
        'date': '2022-01-04',
        'publisher': 'Fox News',
        'writer': 'Yoda'
    }

];
news = sorted(news, key=lambda k: k['date'], reverse=True)

# Home Page
@task_list_blueprint.route("/")
@task_list_blueprint.route("/home")
def home():
    global IS_LOGGED_IN
    company_db = CompanyDB(g.mysql_db, g.mysql_cursor)
    companies = company_db.get_all_companies_abbrev()
    return render_template('home.html', news = news, companies = companies, IS_LOGGED_IN=IS_LOGGED_IN)
  

@task_list_blueprint.route("/about")
def about():
    return render_template('about.html')

@task_list_blueprint.route('/<company>')
def company(company):
    company_db = CompanyDB(g.mysql_db, g.mysql_cursor)
    stock_abbrev = company_db.get_company_by_stock_abbrev(company)
    companies = company_db.get_all_companies_abbrev()
    company_name = company_db.get_company_name(company)
    company_ceo = company_db.get_ceo_name(company)
    company_founded_date = company_db.get_founded_date(company)
    company_founded_location = company_db.get_founded_location(company)
    company_industry = company_db.get_industry(company)
    return render_template('company.html', company=company, stock_abbrev=stock_abbrev, news=news, 
                        companies=companies, company_name=company_name, company_ceo = company_ceo,
                        company_founded_date=company_founded_date, company_founded_location=company_founded_location, company_industry=company_industry)



@task_list_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        if user_db.get_username(username):
            flash('Username taken!', 'danger')
            return redirect(url_for('task_list_blueprint.register'))
        if user_db.get_email(email):
            flash('Email already in use!', 'danger')
            return redirect(url_for('task_list_blueprint.register'))
        user = User(username=username, email=email, password=password)
        user_db.add_user(user)
        flash(f'Account created for {username}!', 'success')
        return redirect(url_for('task_list_blueprint.home'))

    return render_template('register.html', title='Register', form=form)



@task_list_blueprint.route("/favorites", methods=["GET", "POST"])
def favorites():
    favorites_db = FavoritesDB(g.mysql_db, g.mysql_cursor)
    favorites = request.form.get("collection")
    favorites_db.get_collection(favorites)
    return render_template("favorites.html")


@task_list_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    global IS_LOGGED_IN
    form = LoginForm()
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    user = User(username=form.username.data, password=form.password.data, email = form.password.data)
    users_username =form.username.data
    users_password = form.password.data

    if form.validate_on_submit():
        if user_db.validate_user(users_username, users_password):
            flash(f'You have been logged in {form.username.data}!', 'success')
            IS_LOGGED_IN = True
            response = make_response(redirect('/home'))
            response.set_cookie('userID', users_username)
            return response
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@task_list_blueprint.route("/profile", methods=["GET"])
def profile():
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    name = request.cookies.get('userID')
    user_id = user_db.get_usernames_id(name)
    email = user_db.get_usernames_email(name)
    if (user_id['username'] == name):
        return render_template("profile.html", name=name, email=email)

