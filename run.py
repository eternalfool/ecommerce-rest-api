from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import logging
import config

# config.configure_logging_relative('logging.ini')

logging.basicConfig(filename="ecommerce.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)

logger.info("Registering resources")

from resources.sellers import Sellers
from resources.products import Products
from resources.tokens import Tokens

api.add_resource(Sellers, '/sellers')
api.add_resource(Products, '/products')
api.add_resource(Tokens, '/token')


app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://bb3b44179051f6:d239bffa@us-cdbr-iron-east-04' \
                                 '.cleardb.net/heroku_ec028af4a8b795d'
app.config['SECRET_KEY'] = "NotSoSecret"
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
# app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
app.config['SQLALCHEMY_POOL_SIZE'] = 100

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
