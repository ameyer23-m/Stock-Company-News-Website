from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint, redirect, make_response, session
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from datetime import datetime, date, timedelta


from models.companies_modifier import Company, CompanyDB
from models.news_modifier import News, NewsDB
from models.users_modifier import User, UserDB
from models.favorites_modifier import Favorites, FavoritesDB

task_list_blueprint = Blueprint('task_list_blueprint', __name__)


@task_list_blueprint.route("/")
@task_list_blueprint.route("/home")
def home():
    user_id = request.cookies.get('userID')

    favorites_db = FavoritesDB(g.mysql_db, g.mysql_cursor)
    favorites = favorites_db.get_favorites(user_id)

    news_db = NewsDB(g.mysql_db, g.mysql_cursor)
    news = news_db.get_all()
    today = datetime.combine(date.today(), datetime.min.time())
    news = [n for n in news if n['date'] <= today] # Only shows news from today and before
    news = sorted(news, key=lambda k: k['date'], reverse=True) # sort items by date so most recents are shown first

    company_db = CompanyDB(g.mysql_db, g.mysql_cursor)
    companies = company_db.get_all_companies_abbrev()
    return render_template('home.html', news = news, companies = companies, favorites=favorites)


@task_list_blueprint.route("/about")
def about():
    return render_template('about.html')

@task_list_blueprint.route('/<company>')
def company(company):
    user_id = session.get('user_id')

    company_db = CompanyDB(g.mysql_db, g.mysql_cursor)
    stock_abbrev = company_db.get_company_by_stock_abbrev(company)
    companies = company_db.get_all_companies_abbrev()
    company_name = company_db.get_company_name(company)
    company_ceo = company_db.get_ceo_name(company)
    company_founded_date = company_db.get_founded_date(company)
    company_founded_location = company_db.get_founded_location(company)
    company_industry = company_db.get_industry(company)
    company_id = company_db.get_company_id(company)

    favorites_db = FavoritesDB(g.mysql_db, g.mysql_cursor)
    favorites = favorites_db.get_favorites(user_id)

    news_db = NewsDB(g.mysql_db, g.mysql_cursor)
    news = news_db.get_all_by_company(company)
    today = datetime.combine(date.today(), datetime.min.time())
    news = [n for n in news if n.date <= today] # Only shows news from today and before
    news = sorted(news, key=lambda k: k.date, reverse=True) # sort items by date so most recents are shown first

    return render_template('company.html', company=company, stock_abbrev=stock_abbrev, news=news, companies=companies, 
                        company_name=company_name, company_ceo = company_ceo, company_founded_date=company_founded_date,
                        company_founded_location=company_founded_location, company_industry=company_industry,
                        favorites = favorites, favorites_db=favorites_db, user_id=user_id,
                        company_id=company_id)


@task_list_blueprint.route("/add_fav/<company>", methods=["POST"])
def add_fav(company):
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    favorites_db = FavoritesDB(g.mysql_db, g.mysql_cursor)
    company_db = CompanyDB(g.mysql_db, g.mysql_cursor)

    user_id = session.get('user_id')
    print(user_id)

    # creation of the favorite object
    company_id = company_db.get_company_id(company)
    company_id_value = company_id['id']

    # add the favorite to the database if it doesn't exist already
    if not favorites_db.is_favorite(user_id, company_id_value):
        favorites_db.add_favorite(user_id, company_id_value)

    return redirect(url_for('task_list_blueprint.company', company=company))



@task_list_blueprint.route("/remove_fav/<company>", methods=["POST"])
def remove_fav(company):
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    favorites_db = FavoritesDB(g.mysql_db, g.mysql_cursor)
    company_db = CompanyDB(g.mysql_db, g.mysql_cursor)

    user_id = session.get('user_id')

    # remove the favorite from the database
    company_id = company_db.get_company_id(company)
    company_id_value = company_id['id']
    favorites_db.remove_favorite(user_id, company_id_value)

    return redirect(url_for('task_list_blueprint.company', company=company))






@task_list_blueprint.route("/manage-profile", methods=["POST"])
def manage_profile():
    return render_template("manage-profile.html")


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



@task_list_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    users_username = form.username.data
    users_password = form.password.data

    if form.validate_on_submit():
        if user_db.validate_user(users_username, users_password):
            flash(f'You have been logged in {form.username.data}!', 'success')
            user_info = {"username": users_username, "password": form.password.data}
            session['user'] = user_info
            session['user_id'] = user_db.get_id_user(users_username)
            print(session['user_id'])
            return redirect('/home')
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)


# @task_list_blueprint.route("/logout")
# def logout():
#     session.pop('user', None)
#     flash('You have been logged out', 'success')
#     return redirect(url_for('task_list_blueprint.home'))

@task_list_blueprint.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    flash('You have been logged out', 'success')
    return redirect('/home')

@task_list_blueprint.route("/favorites", methods=["GET", "POST"])
def favorites():
    favorites_db = FavoritesDB(g.mysql_db, g.mysql_cursor)
    favorites = request.form.get("collection")
    favorites_db.get_collection(favorites)
    return render_template("favorites.html")


@task_list_blueprint.route("/profile", methods=["GET"])
def profile():
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    session_data = session.get('user')
    username = session_data.get('username')
    user_id = session_data.get('user_id')
    email = user_db.get_usernames_email(username)

    return render_template("profile.html", name=username, email=email, user_id=user_id)


