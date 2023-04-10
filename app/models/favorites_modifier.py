import mysql.connector
from models.companies_modifier import Company, CompanyDB

class Favorite:
    """
    Initialize the favorites object using its stock abbreviation

        CREATE TABLE favorites
        (
            id INT UNSIGNED AUTO_INCREMENT NOT NULL,
            pk_companies INT UNSIGNED NOT NULL
            stock_abbrev VARCHAR(5)
            CONSTRAINT pk_favorites PRIMARY KEY (id)
            CONSTRAINT fk_companies FOREIGN KEY (pk_companies) REFERENCES Users(stock_abbrev)           
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

class favoritesDB:
    """
    This class provides an interface for interacting with a database of artwork.
    """
    def __init__(self, db_conn, db_cursor):
        self._conn = db_conn
        self._cursor = db_cursor