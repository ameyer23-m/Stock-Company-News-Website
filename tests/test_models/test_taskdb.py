from cgi import test
from re import A
from readline import insert_text
from app.models.companies_modifier import Company, CompanyDB

# By using the parameter db_test_client, we automatically get access to our test
#   database provided by the pytest fixture in conftest.py
#   (note the parameter name matches the name of the fixture function).

"""
    Test for favorites table
"""
def test_get_company_by_stock_abbrev(db_test_client):
    conn, cursor = db_test_client
    testdb = CompanyDB(conn, cursor)

    testcompany = Company("Apple", "APPL")
    testdb.add_user(testcompany) # type: ignore

    inserted_company = testdb.get_company_by_stock_abbrev("APPL")

    assert inserted_company["stock_abbrev"] == "APPL"
    assert inserted_company["company"] == "Apple"
    conn.commit()

