from unittest import result
import mysql.connector


class User():
    """
    Initialize a users object using its username and password.
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

    def get_id_user(self, username):
        query_id = 'SELECT id FROM users WHERE username=%s;'
        self._cursor.execute(query_id, (username,))
        id_record = self._cursor.fetchone()
        if id_record is not None:
            return id_record.get('id')
        else:
            return None

    ## Update
    def update_user(self, new_password, new_email, new_username, username):
        update_query = """
            UPDATE users
            SET password=%s, email=%s, username=%s
            WHERE username=%s;
        """
        self._cursor.execute(update_query, (new_password, new_email, new_username, username))
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

    # Delete User
    # def delete_account(self, id):
    #     delete_query = 'DELETE FROM Users WHERE id = %s'
    #     delete_favorites_query = 'DELETE FROM Favorites WHERE id=%s'
    #     self._cursor.execute(delete_query, (id,))
    #     print(self._cursor.rowcount, "record(s) deleted")
    #     self._conn.commit()


    def delete_account(self, user_id):
        delete_favorites_query = 'DELETE FROM favorites WHERE user_id = %s;'
        delete_user_query = 'DELETE FROM users WHERE id = %s;'
        try:
            self._cursor.execute(delete_favorites_query, (user_id,))
            num_favorites_deleted = self._cursor.rowcount
            self._cursor.execute(delete_user_query, (user_id,))
            num_users_deleted = self._cursor.rowcount
            self._conn.commit()
            print(f"Deleted {num_users_deleted} user(s) and {num_favorites_deleted} favorite(s) for user with id {user_id}")
        except Exception as e:
            print(f"Error deleting user and favorites: {e}")
            self._conn.rollback()


    def disconnect(self):
        self._conn.close()