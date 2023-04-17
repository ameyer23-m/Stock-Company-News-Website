import mysql.connector


class Company:
    """
    Initialize the companies object using its company name and stock abbreviation

        companies
        (
            id INT UNSIGNED AUTO_INCREMENT NOT NULL,
            company VARCHAR(40),
            stock_abbrev VARCHAR(5),
            industry VARCHAR(30),
            ceo VARCHAR(40),
            founded_date TIMESTAMP,
            founded_location VARCHAR(50),
            CONSTRAINT pk_companies PRIMARY KEY (id)
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

        companies = self._cursor.fetchall()
        return [company['stock_abbrev'] for company in companies]
    

    def get_company_by_stock_abbrev(self, stock_abbrev):
        get_company_by_stock_abbrev = """
                SELECT stock_abbrev from companies WHERE stock_abbrev = %s;
        """
        self._cursor.execute(get_company_by_stock_abbrev, (stock_abbrev,))
        company = self._cursor.fetchone()

        return company

    def get_company_name(self, stock_abbrev):
        get_company = """
            SELECT company from companies WHERE stock_abbrev = %s;
        """
        self._cursor.execute(get_company, (stock_abbrev,))
        company = self._cursor.fetchone()
        if company is not None:
            return company['company']
        else:
            return None
        

    def get_ceo_name(self, stock_abbrev):
        get_ceo_name = """
            SELECT ceo from companies WHERE stock_abbrev = %s;
        """
        self._cursor.execute(get_ceo_name, (stock_abbrev,))
        company = self._cursor.fetchone()
        if company is not None:
            return company['ceo']
        else:
            return None

    def get_founded_date(self, stock_abbrev):
        get_founded_date = """
            SELECT founded_date from companies WHERE stock_abbrev = %s;
        """
        self._cursor.execute(get_founded_date, (stock_abbrev,))
        company = self._cursor.fetchone()
        if company is not None:
            return company['founded_date']
        else:
            return None

    def get_founded_location(self, stock_abbrev):
        get_founded_location = """
            SELECT founded_location from companies WHERE stock_abbrev = %s;
        """
        self._cursor.execute(get_founded_location, (stock_abbrev,))
        company = self._cursor.fetchone()
        if company is not None:
            return company['founded_location']
        else:
            return None
            

    def get_industry(self, stock_abbrev):
        get_industry = """
            SELECT industry from companies WHERE stock_abbrev = %s;
        """
        self._cursor.execute(get_industry, (stock_abbrev,))
        company = self._cursor.fetchone()
        if company is not None:
            return company['industry']
        else:
            return None


    def add_company(self, new_company):
        insert_user_query = '''
            INSERT INTO companies (company, stock_abbrev, industry, ceo, founded_date, founded_location)
            VALUES (%s, %s, %s, %s, %s, %s);
        '''

        self._cursor.execute(insert_user_query,(new_company._company, new_company._stock_abbrev,
                    new_company._industry, new_company._ceo, new_company._founded_date,
                    new_company._founded_location))
        self._conn.commit()

        print(self._cursor.rowcount, "record(s) affected")

        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        new_user_id = self._cursor.fetchone()

        return new_user_id

    # Not using these because I dont want them in the app, but here are two examples for the other CRUD parts
    def update_ceo(self, new_ceo):
        query_update_description = '''
            INSERT INTO companies (ceo) VALUES (%s);
        '''

        self._cursor.execute(query_update_description, (new_ceo,))
        self._conn.commit()

        self._cursor.execute("SELECT LAST_INSERT_ID() id")
        new_user_id = self._cursor.fetchone()
        # self._cursor.close()

        return new_user_id


    
    def delete_company(self, id):
        query = """ DELETE FROM companies WHERE id=%s;"""

        self._cursor.execute(query, (id,))
        self._conn.commit()
        
        print(self._cursor.rowcount, "record(s) affected")
        # self._cursor.close()

    # def company_check(self, company):
    #     company = self.get_company(company)
    #     if not company:
    #         return False
    #     else:
    #         return True
        
    # def company_user(self, company,stock_abbrev,industry,ceo,founded_date,founded_location):
    #     company_id = self.get_id(company, stock_abbrev, industry, ceo, founded_date, founded_location)
    #     if company_id:
    #         return True
    #     else:
    #         return False

    def disconnect(self):
        self._conn.close()
        

