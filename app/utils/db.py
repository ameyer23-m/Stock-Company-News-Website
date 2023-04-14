"""
Collection of functions to help establish the database
"""
import mysql.connector
import csv

from models.companies_modifier import Company, CompanyDB

# Connect to MySQL and the task database
def connect_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"],
        database=config["DATABASE"]
    )
    return conn


# Setup for the Database
#   Will erase the database if it exists
def init_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"]
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"DROP DATABASE IF EXISTS {config['DATABASE']};")
    cursor.execute(f"CREATE DATABASE {config['DATABASE']};")
    cursor.execute(f"use {config['DATABASE']};")
    cursor.execute(
        f""" 
        CREATE TABLE companies
        (
            id INT UNSIGNED AUTO_INCREMENT NOT NULL,
            company VARCHAR(40),
            stock_abbrev VARCHAR(5),
            industry VARCHAR(30),
            ceo VARCHAR(40),
            founded_date TIMESTAMP,
            founded_location VARCHAR(50),
            CONSTRAINT pk_companies PRIMARY KEY (id)
        );

        CREATE TABLE news
        (
            id INT UNSIGNED AUTO_INCREMENT NOT NULL,
            company_id INT UNSIGNED,
            article VARCHAR(200),
            date TIMESTAMP,
            publisher VARCHAR(50),
            writer VARCHAR(40),
            CONSTRAINT pk_news PRIMARY KEY (id),
            CONSTRAINT fk_companies_news FOREIGN KEY (company_id) REFERENCES companies(id)           
        );

        CREATE TABLE users
        (
            id INT UNSIGNED AUTO_INCREMENT NOT NULL,
            password VARCHAR(255),
            username VARCHAR(30),
            email VARCHAR(30),
            CONSTRAINT pk_users PRIMARY KEY (id)
        );

        CREATE TABLE favorites
        (
            id INT UNSIGNED AUTO_INCREMENT NOT NULL,
            pk_companies INT UNSIGNED NOT NULL,
            user_id INT UNSIGNED,
            CONSTRAINT pk_favorites PRIMARY KEY (id),
            CONSTRAINT fk_companies_favorites FOREIGN KEY (pk_companies) REFERENCES companies(id),
            CONSTRAINT fk_users_favorites FOREIGN KEY (user_id) REFERENCES users(id)        
        );
        """
    )
    cursor.close()
    conn.close()


# def populate_companies(conn, csvfile):
#     cursor = conn.cursor(dictionary=True)
    
#     sql_companies_insert = "INSERT INTO companies (company, stock_abbrev, industry, ceo, founded_date, founded_location) VALUES (%s, %s, %s, %s, %s, %s)"

#     with open(csvfile, "r") as csv_input:
#         reader = csv.DictReader(csv_input)
#         for row in reader:            
#             cursor.execute(sql_companies_insert, (row["company"], row["stock_abbrev"], row["industry"], row["ceo"], row["founded_date"], row["founded_location"]))

#     conn.commit()
#     cursor.close()
#     conn.close()

def populate_companies(conn, cursor, csvfile):
    
    sql_companies_insert = "INSERT INTO companies (company, stock_abbrev, industry, ceo, founded_location) VALUES (%s, %s, %s, %s, %s)"

    with open(csvfile, "r") as csv_input:
        reader = csv.DictReader(csv_input)
        for row in reader:            
            cursor.execute(sql_companies_insert, (row["company"], row["stock_abbrev"], row["industry"], row["ceo"], row["founded_location"]))

    

# def populate_news(conn, cursor, csvfile):
#     # cursor = conn.cursor(dictionary=True)
    
#     sql_news_insert = "INSERT INTO news (company_id, article, date, publisher, writer) VALUES (%i, %s, %s, %s, %s)"
#     sql_companies_find = "SELECT id FROM companies WHERE company=(%s)"

#     with open(csvfile, "r") as csv_input:
#         reader = csv.DictReader(csv_input)
#         for row in reader:
#             cursor.execute(sql_companies_find, (row['company'],))
#             company = cursor.fetchone()
#             print(company)
            
#             # if not company_id:
#             #     continue
#             # company_id = 1
#             cursor.execute(sql_news_insert, (company["id"], row["article"], row["date"], row["publisher"], row["writer"], ))

def populate_news(conn, cursor, csvfile):
    # cursor = conn.cursor(dictionary=True)
    
    sql_news_insert = "INSERT INTO news (company_id) VALUES (%i)"
    sql_companies_find = "SELECT id FROM companies WHERE company=(%s)"

    with open(csvfile, "r") as csv_input:
        reader = csv.DictReader(csv_input)
        for row in reader:
            cursor.execute(sql_companies_find, (row['company'],))
            company = cursor.fetchone()
            print(company)
            # if CompanyDB.company_check:
            #     continue
            # else:
            # # if not company_id:
            # #     continue
            # # company_id = 1
            cursor.execute(sql_news_insert, (company["id"], ))

    
    

def seed_db(config):
    conn = connect_db(config)
    cursor = conn.cursor(dictionary=True, buffered=True)
    populate_companies(conn, cursor, "./csv/companies.csv")
    populate_news(conn, cursor, "./csv/company_news.csv")
    conn.commit()
    cursor.close()
    conn.close()
