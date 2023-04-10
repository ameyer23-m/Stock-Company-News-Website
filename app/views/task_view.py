from flask import Blueprint, request, redirect
from flask import render_template, g, Blueprint
from models.task import Task, TaskDB
from models.companies_modifier import Company, CompanyDB

task_list_blueprint = Blueprint('task_list_blueprint', __name__)

# Home Page
# @task_list_blueprint.route("/")
# def index():
#     return render_template("index.html")

@task_list_blueprint.route('/', methods=["GET", "POST"])
def index():
    company_db = CompanyDB(g.mysql_db, g.mysql_cursor)

    # if request.method == "POST":
    #     task_ids = request.form.getlist("task_item")
    #     for id in task_ids:
    #         database.delete_task_by_id(id)

    return render_template('index.html')    

