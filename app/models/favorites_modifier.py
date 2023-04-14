import mysql.connector
from models.companies_modifier import Company, CompanyDB

class Favorite:
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

    def add_favorites(self, user_id):
        """
        Add a new company to the favorites list for a specified user

        :param user
        """
        insert_fav_query = '''
            INSERT INTO favorites (user_id, pk_companies)
            VALURES (%s, %s);
        '''

        self._cursor.execute(insert_fav_query, (user_id, Company.Company_id))
        self._conn.commit()
        print(self._cursor.rowcount, "record(s) affected")

        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        new_user_id = self._cursor.fetchone()
        # self._cursor.close()
        return new_user_id



    def delete_artwork(self, id):
        """
        Remove a artwork record from the database
        
        :param id: id of the artwork to be removed from the database
        """
        query = 'DELETE FROM favorites WHERE id=%s;'


        self._cursor.execute(query, (id,))
        self._conn.commit()
        
        print(self._cursor.rowcount, "record(s) affected")
        # self._cursor.close()

    def disconnect(self):
        self._conn.close()