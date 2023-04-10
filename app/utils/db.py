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
            founded_date timestamp,
            founded_location VARCHAR(50),
            CONSTRAINT pk_companies PRIMARY KEY (id),
        );
        """
    )

    # cursor.execute(
    #     f""" 
    #     CREATE TABLE favorites
    #     (
    #         id INT UNSIGNED AUTO_INCREMENT NOT NULL,
    #         pk_companies INT UNSIGNED NOT NULL
    #         stock_abbrev VARCHAR(5)
    #         CONSTRAINT pk_favorites PRIMARY KEY (id)
    #         CONSTRAINT fk_companies FOREIGN KEY (pk_companies) REFERENCES Company(id)           
    #     );
    #     """
    # )

    # cursor.execute(
    #     f""" 
    #     CREATE TABLE news
    #     (
    #         id INT UNSIGNED AUTO_INCREMENT NOT NULL,
    #         company VARCHAR(40),
    #         article VARCHAR(200),
    #         date timestamp,
    #         publisher VARCHAR(50),
    #         writer VARCHAR(40),
    #         CONSTRAINT pk_favorites PRIMARY KEY (id)
    #         CONSTRAINT fk_companies FOREIGN KEY (pk_companies) REFERENCES Users(company)           
    #     );
    #     """
    # )
    cursor.close()
    conn.close()
