"""
Collection of functions to help establish the database
"""
import mysql.connector


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
