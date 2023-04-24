from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint, redirect, make_response, session
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, ManageAccountForm
from datetime import datetime, date, timedelta


from models.companies_modifier import Company, CompanyDB
from models.news_modifier import News, NewsDB
from models.users_modifier import User, UserDB
from models.favorites_modifier import Favorites, FavoritesDB

task_list_blueprint = Blueprint('task_list_blueprint', __name__)


@task_list_blueprint.route("/")
@task_list_blueprint.route("/home")
def home():
    user_id = session.get('user_id')

    news_db = NewsDB(g.mysql_db, g.mysql_cursor)
    news = news_db.get_all()
    today = datetime.combine(date.today(), datetime.min.time())
    news = [n for n in news if n['date'] <= today] # Only shows news from today and before
    news = sorted(news, key=lambda k: k['date'], reverse=True) # sort items by date so most recents are shown first

    company_db = CompanyDB(g.mysql_db, g.mysql_cursor)
    companies = company_db.get_all_companies_abbrev()
    return render_template('home.html', news = news, companies = companies)





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


    news_db = NewsDB(g.mysql_db, g.mysql_cursor)
    news = news_db.get_all_by_company(company)
    today = datetime.combine(date.today(), datetime.min.time())
    news = [n for n in news if n.date <= today] # Only shows news from today and before
    news = sorted(news, key=lambda k: k.date, reverse=True) # sort items by date so most recents are shown first

    return render_template('company.html', company=company, stock_abbrev=stock_abbrev, news=news, companies=companies, 
                        company_name=company_name, company_ceo = company_ceo, company_founded_date=company_founded_date,
                        company_founded_location=company_founded_location, company_industry=company_industry, user_id=user_id,
                        company_id=company_id)





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
        return redirect(url_for('task_list_blueprint.login'))

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
            session['user'] = users_username
            session['password'] = form.password.data
            session['user_id'] = user_db.get_id_user(users_username)
            session['email'] = user_db.get_usernames_email(users_username)
            print(session['user_id'])
            return redirect('/home')
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html', title='Login', form=form)






@task_list_blueprint.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    flash('You have been logged out', 'success')
    return redirect('/home')





@task_list_blueprint.route("/profile", methods=['GET', 'POST'])
def profile():
    user = session.get('user')
    password = session.get('password')
    email = session.get('email')

    return render_template('profile.html', user=user, password=password, email=email)



@task_list_blueprint.route("/manage_account", methods=['GET', 'POST'])
def manage_account():
    form = ManageAccountForm()
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    username = session.get('user')
    email = session.get('email')

    if form.validate_on_submit():
        new_username = form.new_username.data
        new_password = form.new_password.data
        new_email = form.new_email.data

        if username != new_username:
            if user_db.get_username(new_username):
                flash('Username taken!', 'danger')
                return redirect(url_for('task_list_blueprint.manage_account'))

        if email != new_email:
            if user_db.get_email(new_email):
                flash('Email already in use!', 'danger')
                return redirect(url_for('task_list_blueprint.manage_account'))

        user_db.update_user(new_password, new_email, new_username, username)
        flash(f'Account updated for {new_username}!', 'success')

        # update session variables
        session['user'] = new_username
        session['password'] = new_password
        session['email'] = new_email

        return redirect(url_for('task_list_blueprint.home'))

    return render_template('manage_account.html', title='Manage Account', form=form)


@task_list_blueprint.route("/delete_account_warning", methods=['GET', 'POST'])
def delete_account_warning():
    username = session.get('user')
    return render_template('delete_account_warning.html', username=username)


@task_list_blueprint.route("/delete_account", methods=['GET', 'POST'])
def delete_account():
    user_id = session.get('user_id')
    user_db = UserDB(g.mysql_db, g.mysql_cursor)
    user_db.delete_account(user_id)
    session.pop('user', None)
    flash('Your account has been deleted', 'success')
    return redirect('/home')