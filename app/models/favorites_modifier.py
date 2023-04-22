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

    def get_favorites(self, user_id):
        get_favorites = """
        SELECT pk_companies FROM favorites WHERE user_id = %s
        """
        self._cursor.execute(get_favorites, (user_id,))
        favorites = self._cursor.fetchall()
        return favorites

    def is_favorite(self, user_id, company_id):
        query = 'SELECT * FROM favorites WHERE user_id = %s AND pk_companies = %s'
        self._cursor.execute(query, (user_id, company_id))
        return self._cursor.fetchone() is not None

    def add_favorite(self, user_id, company_id):
        insert_fav_query = '''
            INSERT INTO favorites (user_id, pk_companies)
            VALUES (%s, %s);
        '''
        self._cursor.execute(insert_fav_query, (user_id, company_id))
        self._conn.commit()
        print(self._cursor.rowcount, "record(s) affected")
        return company_id

    def remove_favorite(self, user_id, company_id):
        delete_fav_query = '''
            DELETE FROM favorites WHERE user_id = %s AND pk_companies = %s;
        '''
        self._cursor.execute(delete_fav_query, (user_id, company_id))
        self._conn.commit()
        print(self._cursor.rowcount, "record(s) deleted")



    # def delete_artwork(self, id):
    #     query = 'DELETE FROM favorites WHERE id=%s;'
    #     self._cursor.execute(query, (id,))
    #     self._conn.commit()
    #     print(self._cursor.rowcount, "record(s) affected")
        

    def disconnect(self):
        self._conn.close()