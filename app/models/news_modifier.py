import mysql.connector


class News:
    """
    Initialize the news object
    """

    def __init__(self, company_id, article, date, publisher, writer):
        self._company = company_id
        self._article = article
        self._date = date
        self._publisher = publisher
        self._writer = writer
    
    @property
    def company(self):
        return self._company

    @property
    def article(self):
        return self._article

    @property
    def date(self):
        return self._date
    
    @property
    def publisher(self):
        return self._publisher

    @property
    def writer(self):
        return self._writer

    @property
    def id(self):
        return self._id

class NewsDB:
    """
    This class provides an interface for interacting with a database of News.
    """
    def __init__(self, db_conn, db_cursor):
        self._conn = db_conn
        self._cursor = db_cursor

    def get_all(self):
        """
        This gets all the news articles
        """
        select_all = """
        SELECT * from news;
        """
        self._cursor.execute(select_all)
        news = self._cursor.fetchall()
        return news

    def get_all_by_company(self, stock_abbrev):
        """
        Gets all the news items for a certain company.

        Args:
            param1: The Stock Symbol

        Returns:
            Each new item in the db with the specified stock symbol
        """
        select_all_by_comp = """
        SELECT news.*, companies.company 
        FROM news 
        JOIN companies ON news.company_id = companies.id
        WHERE companies.stock_abbrev = %s;
        """
        self._cursor.execute(select_all_by_comp, (stock_abbrev,))
        news = self._cursor.fetchall()
        return [News(int(n['company_id']), n['article'], n['date'], n['publisher'], n['writer']) for n in news]

    def disconnect(self):
        self._conn.close()
