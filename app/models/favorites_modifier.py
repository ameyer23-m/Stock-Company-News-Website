"""
Will be used later but not for the final version for the cs232 class
"""

import mysql.connector
from models.companies_modifier import Company, CompanyDB


class Favorites:
    """
    Initialize the favorites object using its stock abbreviation

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

    def __init__(self, Company_id, stock_abbrev, id=None):
        self._Company_id = Company_id
        self._stock_abbrev = stock_abbrev
        self._id = id
    
    @property
    def Company_id(self):
        return self._Company_id

    @property
    def stock_abbrev(self):
        return self._stock_abbrev

    @property
    def id(self):
        return self._id

class FavoritesDB:
    """
    This class provides an interface for interacting with a database of artwork.
    """
    def __init__(self, db_conn, db_cursor):
        self._conn = db_conn
        self._cursor = db_cursor

        

    def disconnect(self):
        self._conn.close()