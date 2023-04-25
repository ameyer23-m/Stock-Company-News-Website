from cgi import test
from re import A
from readline import insert_text
# from app.models.companies_modifier import Company, CompanyDB
from app.models.users_modifier import User, UserDB
# from app.models.news_modifier import News, NewsDB


# By using the parameter db_test_client, we automatically get access to our test
#   database provided by the pytest fixture in conftest.py
#   (note the parameter name matches the name of the fixture function).


# Insert Company test here



# Insert News test here

"""
    Test for User table
"""
def test_userdb_insert_user(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    testuser = User("isaacschwartz", "fakepassword") # type: ignore
    testdb.add_user(testuser)

    inserteduser = testdb.get_username("isaacschwartz")

    assert inserteduser["username"] == "isaacschwartz"
    assert inserteduser["password"] == "fakepassword"
    conn.commit()


def test_userdb_check_user(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    assert testdb.user_check("isaacschwartz") == True # type: ignore
    assert testdb.user_check("ischwartz23@wooster.edu") == False # type: ignore
    conn.commit()


def test_userdb_validate_user(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    assert testdb.validate_user("isaacschwartz", "fakepassword") == True
    assert testdb.validate_user("ischwartz23@wooster.edu", "fkaepw") == False
    conn.commit()


def test_userdb_delete_user(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    testuser = User("isaacschwartz2", "fakepassword") # type: ignore
    testdb.add_user(testuser)

    insertuser = testdb.get_username("isaacschwartz2")
    testdb.delete_user(insertuser['id']) # type: ignore

    assert testdb.user_check("isaacschwartz") == True # type: ignore
    assert testdb.user_check("isaacschwartz2") == False # type: ignore
    conn.commit()


def test_userdb_update_password(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    inserteduser = testdb.get_username("isaacschwartz")
    testdb.update_password(inserteduser['id'], "new_password") # type: ignore
    update_password = testdb.get_username("isaacschwartz")

    assert update_password["password"] == "new_password"   
    conn.commit()


def test_userdb_update_firstname(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    inserteduser = testdb.get_username("isaacschwartz")
    testdb.update_first_name(inserteduser['id'], "Isaac") # type: ignore
    update_firstname = testdb.get_username("isaacschwartz")

    assert update_firstname["first_name"] == "Isaac"
    conn.commit()


def test_userdb_update_lastname(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    inserteduser = testdb.get_username("isaacschwartz")
    testdb.update_last_name(inserteduser['id'], "Schwartz") # type: ignore
    update_lastname = testdb.get_username("isaacschwartz")

    assert update_lastname["last_name"] == "Schwartz"
    conn.commit()


def test_userdb_update_email(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    inserteduser = testdb.get_username("isaacschwartz")
    testdb.update_email(inserteduser['id'], "ischwartz23@wooster.edu") # type: ignore
    update_email = testdb.get_username("isaacschwartz")

    assert update_email["email"] == "ischwartz23@wooster.edu"
    conn.commit()


def test_userdb_update_description(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    inserteduser = testdb.get_username("isaacschwartz")
    testdb.update_description(inserteduser['id'], "test description") # type: ignore
    update_description = testdb.get_username("isaacschwartz")

    assert update_description["description"] == "test description"
    conn.commit()
