from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint, redirect, make_response
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from datetime import datetime, date, timedelta


from models.companies_modifier import Company, CompanyDB
from models.news_modifier import News, NewsDB
from models.users_modifier import User, UserDB

task_list_blueprint = Blueprint('task_list_blueprint', __name__)

IS_LOGGED_IN = False;


@task_list_blueprint.route("/")
@task_list_blueprint.route("/home")
def home():
    global IS_LOGGED_IN
    news_db = NewsDB(g.mysql_db, g.mysql_cursor)
    news = news_db.get_all()
    today = datetime.combine(date.today(), datetime.min.time())
    news = [n for n in news if n['date'] <= today] # Only shows news from today and before
    news = sorted(news, key=lambda k: k['date'], reverse=True) # sort items by date so most recents are shown first

    company_db = CompanyDB(g.mysql_db, g.mysql_cursor)
    companies = company_db.get_all_companies_abbrev()
    return render_template('home.html', news = news, companies = companies, IS_LOGGED_IN=IS_LOGGED_IN)


@task_list_blueprint.route("/about")
def about():
    global IS_LOGGED_IN
    return render_template('about.html', IS_LOGGED_IN=IS_LOGGED_IN)

@task_list_blueprint.route('/<company>')
def company(company):
    global IS_LOGGED_IN
    
    company_db = CompanyDB(g.mysql_db, g.mysql_cursor)
    stock_abbrev = company_db.get_company_by_stock_abbrev(company)
    companies = company_db.get_all_companies_abbrev()
    company_name = company_db.get_company_name(company)
    company_ceo = company_db.get_ceo_name(company)
    company_founded_date = company_db.get_founded_date(company)
    company_founded_location = company_db.get_founded_location(company)
    company_industry = company_db.get_industry(company)

    news_db = NewsDB(g.mysql_db, g.mysql_cursor)
    news = news_db.get_all_by_company(company)
    today = datetime.combine(date.today(), datetime.min.time())
    news = [n for n in news if n.date <= today] # Only shows news from today and before
    news = sorted(news, key=lambda k: k.date, reverse=True) # sort items by date so most recents are shown first
    return render_template('company.html', company=company, stock_abbrev=stock_abbrev, news=news, 
                        companies=companies, company_name=company_name, company_ceo = company_ceo,
                        company_founded_date=company_founded_date, company_founded_location=company_founded_location, 
                        company_industry=company_industry, IS_LOGGED_IN=IS_LOGGED_IN)



@task_list_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    global IS_LOGGED_IN
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

    return render_template('register.html', title='Register', form=form, IS_LOGGED_IN=IS_LOGGED_IN)



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
    return render_template('login.html', title='Login', form=form, IS_LOGGED_IN=IS_LOGGED_IN)

@task_list_blueprint.route("/profile", methods=["GET"])
def profile():
    global IS_LOGGED_IN
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    name = request.cookies.get('userID')
    user_id = user_db.get_usernames_id(name)
    email = user_db.get_usernames_email(name)
    if (user_id['username'] == name):
        return render_template("profile.html", name=name, email=email, IS_LOGGED_IN=IS_LOGGED_IN)

