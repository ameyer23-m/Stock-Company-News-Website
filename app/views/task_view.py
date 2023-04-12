from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
from models.task import Task, TaskDB
from models.companies_modifier import Company, CompanyDB
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

task_list_blueprint = Blueprint('task_list_blueprint', __name__)

news = [
    {
        'company': 'APPL',
        'article': 'Article 1 on APPL',
        'date': '2022-01-03',
        'publisher': 'NY Times',
        'writer': 'Joe Biden'
    },
    {
        'company': 'APPL',
        'article': 'Article 2 on APPL',
        'date': '2022-01-04',
        'publisher': 'NY Times',
        'writer': 'Joe Biden'
    },
    {
        'company': 'MSFT',
        'article': 'Article 1 on MSFT ',
        'date': '2022-01-04',
        'publisher': 'Time Magazine',
        'writer': 'Susan Test'
    },
    {
        'company': 'MSFT',
        'article': 'Article 2 on MSFT ',
        'date': '2022-01-10',
        'publisher': 'Time Magazine',
        'writer': 'Susan Test'
    },
    {
        'company': 'MSFT',
        'article': 'Article 3 on MSFT ',
        'date': '2022-04-04',
        'publisher': 'NBC',
        'writer': 'Jon Snow'
    },
    {
        'company': 'JPM',
        'article': 'Article 1 on JPM ',
        'date': '2022-01-04',
        'publisher': 'Fox News',
        'writer': 'Yoda'
    }

];
news = sorted(news, key=lambda k: k['date'], reverse=True)

companies = ['APPL', 'XOM', 'MSFT', 'GE', 'JPM']

# Home Page
@task_list_blueprint.route("/")
@task_list_blueprint.route("/home")
def home():
    return render_template('home.html', news = news, companies = companies)

@task_list_blueprint.route("/about")
def about():
    return render_template('about.html')

@task_list_blueprint.route('/<company>')
def company(company):
    return render_template('company.html', company=company, news = news)


@task_list_blueprint.context_processor
def inject_companies():
    return dict(companies=companies)

@task_list_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@task_list_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@investinsights.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
