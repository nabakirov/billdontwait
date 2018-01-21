from flask import Flask

app = Flask(__name__)

from Bill.configs import DB_PATH, conn_props
# from Bill.dataBase import DB
from Bill.postges import DB

db = DB(conn_props)

from Bill import api
from Bill import views