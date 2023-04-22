import mysql.connector


class News:
    """
    Initialize the news object
         news
        (
            id INT UNSIGNED AUTO_INCREMENT NOT NULL,
            company_id INT UNSIGNED,
            article VARCHAR(200),
            date DATETIME,
            publisher VARCHAR(50),
            writer VARCHAR(40),
            CONSTRAINT pk_news PRIMARY KEY (id),
            CONSTRAINT fk_companies_news FOREIGN KEY (company_id) REFERENCES companies(id)           
        );
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
        select_all = """
        SELECT * from news;
        """
        self._cursor.execute(select_all)
        news = self._cursor.fetchall()
        return news

    def get_all_by_company(self, stock_abbrev):
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
