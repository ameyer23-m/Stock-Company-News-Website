from unittest import result
import mysql.connector


class User():
    """
    Initialize a users object using its username and password.
    users
        (
            id INT UNSIGNED AUTO_INCREMENT NOT NULL,
            password VARCHAR(255),
            username VARCHAR(30),
            email VARCHAR(30),
            CONSTRAINT pk_users PRIMARY KEY (id)
        );
    """
    def __init__(self, password, username, email, id=None):
        self._password = password
        self._username = username
        self._email = email
        self._id = id
    

    @property
    def password(self):
        return self._password

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def id(self):
        return self._id

class UserDB:
    """
    This class provides an interface for interacting with a database of Users.
    """

    def __init__(self, db_conn, db_cursor):
        self._conn = db_conn
        self._cursor = db_cursor
    
    ## Get 
    def get_username(self, user_name):
        query_username = 'SELECT * FROM users WHERE username=%s;'
        self._cursor.execute(query_username, (user_name,))
        username_record = self._cursor.fetchone()
        return username_record

    def get_email(self, email):
        query_email = 'SELECT * FROM users WHERE email=%s;'
        self._cursor.execute(query_email, (email,))
        email_record = self._cursor.fetchone()
        return email_record

    def get_usernames_id(self, username):
        query_id = 'SELECT * FROM users WHERE username=%s;'
        self._cursor.execute(query_id, (username,))
        id_record = self._cursor.fetchone()
        return id_record

    def get_id(self, username, password):
        id_record = 0
        query_id = 'SELECT * FROM users WHERE username=%s and password=%s;'
        self._cursor.execute(query_id, (username, password))
        id_record = self._cursor.fetchone()
        return id_record
    
    def get_password(self, pass_word):
        query_password = 'SELECT * FROM users WHERE password=%s;'
        self._cursor.execute(query_password, (pass_word,))
        password_record = self._cursor.fetchone()
        return password_record

    def get_usernames_id(self, username):
        query_id = 'SELECT id FROM Users WHERE username=%s;'
        self._cursor.execute(query_id, (username,))
        id_record = self._cursor.fetchone()
        return id_record['id'] if id_record else None

    def get_usernames_email(self, username):
        query_id = 'SELECT email FROM Users WHERE username=%s;'
        self._cursor.execute(query_id, (username,))
        record = self._cursor.fetchone()
        return record['email'] if record else None

    ## Update
    def update_password(self, new_password, id):
        update_query = """
            UPDATE users
            SET password=%s
            WHERE id=%s;
        """
        self._cursor.execute(update_query, (new_password, id))
        self._conn.commit()
        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        user_id = self._cursor.fetchone()


    def update_email(self, id, new_email):
        update_query = """
            UPDATE users
            SET email=%s
            WHERE id=%s;
        """
        self._cursor.execute(update_query, (new_email, id))
        self._conn.commit()
        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        user_id = self._cursor.fetchone()
        return user_id

    ## Add
    def add_user(self, accounts):  #------------------------------ used
        """
        Add a new users username record to the database
        """
        insert_user_query = '''
            INSERT INTO users (username, password, email)
            VALUES (%s, %s, %s);
        '''
        self._cursor.execute(insert_user_query, (accounts._username, accounts._password, accounts._email))
        self._conn.commit()
        print(self._cursor.rowcount, "record(s) affected")
        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        new_user_id = self._cursor.fetchone()
        return new_user_id

    def get_id_user(self, username):
        query_id = 'SELECT id FROM users WHERE username=%s;'
        self._cursor.execute(query_id, (username,))
        id_record = self._cursor.fetchone()
        if id_record is not None:
            return id_record.get('id')
        else:
            return None

    ## Deleting 
    # def delete_user(self, id):
    #     """
    #     Remove a user record from the database
    #     """
    #     query = 'DELETE FROM users WHERE id=%s;'
    #     query1 = 'DELETE FROM artwork WHERE id=%s'
    #     query2 = 'DELETE FROM CollectionExhibit WHERE id=%s'
    #     query3 = '''SELECT users.id as user_id, artwork.id as artwork_id, 
    #                 collectionexhibit.id as collection_id FROM users 
    #                 inner join artwork on users.id = artwork.pk_users inner join 
    #                 collectionexhibit on collectionexhibit.pk_artwork = artwork.id WHERE users.id = %s;'''
        

    #     self._cursor.execute(query3, (id,))
    #     result_set = self._cursor.fetchall()
    #     for result in result_set:
    #         self._cursor.execute(query2, (result['collection_id'],))
    #         self._cursor.execute(query1, (result['artwork_id'],))
    #     self._cursor.execute(query, (id,))
    #     self._conn.commit()
        
    #     print(self._cursor.rowcount, "record(s) affected")

    ## Sign in validations
    def user_check(self, user_name):
        person = self.get_username(user_name)
        if not person:
            return False
        else:
            return True
        
    def validate_user(self, user_name, given_password): # ----------------------------- used
        persons_id = self.get_id(user_name, given_password)
        if persons_id:
            return True
        else:
            return False

    def validate_email(self, email):
        person = self.get_email(email)
        if person:
            return True
        else:
            return False


    def disconnect(self):
        self._conn.close()