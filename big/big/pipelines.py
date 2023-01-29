# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector


class BigPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            database = 'books')
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS books_tb""")
        self.curr.execute("""create table books_tb(
                        product_name text UNIQUE,
                        product_author text,
                        product_price text,
                        product_imagelink text,
                        product_rating VARCHAR(3),
                        product_valuation text,
                        product_link text
                        )""")

    def process_item(self, items, spider):
        self.store_db(items)
        return items
    
    def store_db(self, items):
        self.curr.execute("""INSERT INTO books_tb values (%s,%s,%s,%s,%s,%s,%s)""",(
            items['product_name'][0],
            items['product_author'][0],
            items['product_price'][0],
            items['product_imagelink'][0],
            items['product_rating'][0],
            items['product_valuation'][0],
            items['product_link'][0]
        ))
        self.conn.commit()