import mysql.connector


class Company:
    """
    Initialize the companies object using its company name and stock abbreviation

        CREATE TABLE companies
        (
            id INT UNSIGNED AUTO_INCREMENT NOT NULL,
            company VARCHAR(40),
            stock_abbrev VARCHAR(5),
            industry VARCHAR(30),
            ceo VARCHAR(40),
            founded_date timestamp,
            founded_location VARCHAR(50),
            CONSTRAINT pk_companies PRIMARY KEY (id),
        );
    """
    def __init__(self, company, stock_abbrev, industry=None, ceo=None, founded_date=None, founded_location=None, id=None):
        self._company = company
        self._stock_abbrev = stock_abbrev
        self._industry = industry
        self._ceo = ceo
        self._founded_date = founded_date
        self._founded_location = founded_location
        self._id = id

    @property
    def company(self):
        return self._company

    @property
    def stock_abbrev(self):
        return self._stock_abbrev

    @property
    def industry(self):
        return self._industry
        
    @property
    def ceo(self):
        return self._ceo

    @property
    def founded_date(self):
        return self._founded_date

    @property
    def founded_location(self):
        return self._founded_location

    @property
    def id(self):
        return self._id

class CompanyDB:
    """
    This class provides an interface for interacting with a database of Users.
    """
    def __init__(self, db_conn, db_cursor):
        self._conn = db_conn
        self._cursor = db_cursor

    
    def get_all_companies_abbrev(self):
        select_all_abbrev_query = """
            SELECT stock_abbrev from companies;
        """
        self._cursor.execute(select_all_abbrev_query)

        return self._cursor.fetchall()
    
    def get_company_by_stock_abbrev(self, stock_abbrev):
        get_company_by_stock_abbrev = """
                SELECT stock_abbrev from companies WHERE id = %s;
        """
        self._cursor.execute(get_company_by_stock_abbrev, (stock_abbrev,))
        company = self._cursor.fetchone()

        return company

