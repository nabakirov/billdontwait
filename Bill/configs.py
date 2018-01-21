from os import environ
DB_PATH = 'DataBases/data.db'

test = "dbname='dev' user='dev' password='dev'"

conn_props = environ.get('DATABASE_URL', test)