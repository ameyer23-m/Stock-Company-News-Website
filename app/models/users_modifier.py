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
        """
        Checks if the username is in the db.

        Args:
            param1: the usernme.

        Returns:
            The username.
        """
        query_username = 'SELECT * FROM users WHERE username=%s;'
        self._cursor.execute(query_username, (user_name,))
        username_record = self._cursor.fetchone()
        return username_record

    def get_email(self, email):
        """
        Checks if the email is in the db.

        Args:
            param1: the email.

        Returns:
            The email.
        """
        query_email = 'SELECT * FROM users WHERE email=%s;'
        self._cursor.execute(query_email, (email,))
        email_record = self._cursor.fetchone()
        return email_record

    def get_id(self, username, password):
        """
        get the users id for the validate user function

        Args:
            param1: the username
            param2: the password

        Returns:
            The db id corresponding with the username and password.
        """
        id_record = 0
        query_id = 'SELECT * FROM users WHERE username=%s and password=%s;'
        self._cursor.execute(query_id, (username, password))
        id_record = self._cursor.fetchone()
        return id_record

    def get_usernames_email(self, username):
        """
        Finds the email of the user

        Args:
            param1: the username.

        Returns:
            The email or None.
        """
        query_id = 'SELECT email FROM Users WHERE username=%s;'
        self._cursor.execute(query_id, (username,))
        record = self._cursor.fetchone()
        return record['email'] if record else None

    def get_id_user(self, username):
        """
        Finds the id of the username

        Args:
            param1: the username.

        Returns:
            The id or None.
        """
        query_id = 'SELECT id FROM users WHERE username=%s;'
        self._cursor.execute(query_id, (username,))
        id_record = self._cursor.fetchone()
        if id_record is not None:
            return id_record.get('id')
        else:
            return None

    ## Update
    def update_user(self, new_password, new_email, new_username, username):
        """
        Updates the users information.

        Args:
            param1: the new password
            param2: the new email
            param3: the new username
            param4: the original username

        Returns:
            The user id.
        """
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
        
        Args:
            param1: the accounts which included the username, password, and email

        Returns:
            The user id.
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

    def validate_user(self, user_name, given_password):
        """
        Checks that the username and password exist in the same row
        
        Args:
            param1: the username
            param2: the password

        Returns:
            Boolean true or false.
        """
        persons_id = self.get_id(user_name, given_password)
        if persons_id:
            return True
        else:
            return False

    # Delete User
    def delete_account(self, user_id):
        """
        Deletes the Users account
        
        Args:
            param1: the user id

        Returns:
            Error is it doesnt exist.
        """
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
        