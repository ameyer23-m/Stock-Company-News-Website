from cgi import test
from re import A
from readline import insert_text
from app.models.user_db_modifier import User, UserDB
from app.models.artwork_db_modifier import ArtWork, artworkDB
from app.models.ArtCollection_db_modifier import ArtCollection, ArtCollectionDB

# By using the parameter db_test_client, we automatically get access to our test
#   database provided by the pytest fixture in conftest.py
#   (note the parameter name matches the name of the fixture function).

"""
    Test for User table
"""
def test_userdb_insert_user(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    testuser = User("ethankramer", "fakepassword")
    testdb.add_user(testuser)

    inserteduser = testdb.get_username("ethankramer")

    assert inserteduser["username"] == "ethankramer"
    assert inserteduser["password"] == "fakepassword"
    conn.commit()


def test_userdb_check_user(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    assert testdb.user_check("ethankramer") == True
    assert testdb.user_check("erick") == False
    conn.commit()


def test_userdb_validate_user(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    assert testdb.validate_user("ethankramer", "fakepassword") == True
    assert testdb.validate_user("alex", "yooo") == False
    conn.commit()


def test_userdb_delete_user(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    testuser = User("ethankramer2", "fakepassword")
    testdb.add_user(testuser)

    insertuser = testdb.get_username("ethankramer2")
    testdb.delete_user(insertuser['id'])

    assert testdb.user_check("ethankramer") == True
    assert testdb.user_check("ethankramer2") == False
    conn.commit()


def test_userdb_update_password(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    inserteduser = testdb.get_username("ethankramer")
    testdb.update_password(inserteduser['id'], "new_password")
    update_password = testdb.get_username("ethankramer")

    assert update_password["password"] == "new_password"   
    conn.commit()


def test_userdb_update_firstname(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    inserteduser = testdb.get_username("ethankramer")
    testdb.update_first_name(inserteduser['id'], "Ethan")
    update_firstname = testdb.get_username("ethankramer")

    assert update_firstname["first_name"] == "Ethan"
    conn.commit()


def test_userdb_update_lastname(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    inserteduser = testdb.get_username("ethankramer")
    testdb.update_last_name(inserteduser['id'], "kramer")
    update_lastname = testdb.get_username("ethankramer")

    assert update_lastname["last_name"] == "kramer"
    conn.commit()


def test_userdb_update_email(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    inserteduser = testdb.get_username("ethankramer")
    testdb.update_email(inserteduser['id'], "ekramer24@wooster.edu")
    update_email = testdb.get_username("ethankramer")

    assert update_email["email"] == "ekramer24@wooster.edu"
    conn.commit()


def test_userdb_update_description(db_test_client):
    conn, cursor = db_test_client
    testdb = UserDB(conn, cursor)

    inserteduser = testdb.get_username("ethankramer")
    testdb.update_description(inserteduser['id'], "test description")
    update_description = testdb.get_username("ethankramer")

    assert update_description["description"] == "test description"
    conn.commit()

"""
    Test for ArtWork table
"""
def test_artworkdb_add_artwork(db_test_client):
    conn, cursor = db_test_client
    test_artworkdb = artworkDB(conn, cursor)
    test_usersdb = UserDB(conn, cursor)

    inserteduser = test_usersdb.get_username("ethankramer")
    test_artwork = ArtWork(inserteduser['id'], "https://cdn.pixabay.com/photo/2017/08/30/12/45/girl-2696947__480.jpg", "I am mega man", "2022-05-12 10:32:36.003875", "digital", "my collection")
    test_artworkdb.add_artwork(test_artwork)

    inserted_artwork = test_artworkdb.get_artwork("digital", "my collection")

    assert inserted_artwork["pk_users"] == 1
    assert inserted_artwork["img_url"] == "https://cdn.pixabay.com/photo/2017/08/30/12/45/girl-2696947__480.jpg"
    assert inserted_artwork["description"] == "I am mega man"
    assert inserted_artwork["timestamp"] == "2022-05-12 10:32:36.003875"
    assert inserted_artwork["style"] == "digital"
    assert inserted_artwork["exhibit_name"] == "my collection"
    conn.commit()


"""
    Test for ArtCollection table
"""
def test_artcollectiondb_add_artcollection(db_test_client):
    conn, cursor = db_test_client
    test_artworkdb = artworkDB(conn, cursor)
    test_collectiondb = ArtCollectionDB(conn, cursor)

    artwork_id = test_artworkdb.get_artwork("digital", "my collection")

    inserted_collection = ArtCollection("exhibition_name", "my collection description")
    test_collectiondb.add_art_collection(artwork_id['id'], inserted_collection)

    inserted_collection = test_collectiondb.get_collection("exhibition_name")

    inserted_collection["pk_artwork"] == 1 
    inserted_collection["exhibit_name"] == "my collection"
    inserted_collection["description"] == "my collection description"  
    conn.commit()
