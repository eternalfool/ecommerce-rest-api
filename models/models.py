from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
import logging
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey

auth = HTTPBasicAuth()
logger = logging.getLogger(__name__)
app = Flask(__name__)
Base = declarative_base()

engine = create_engine(
    'mysql://bb3b44179051f6:d239bffa@us-cdbr-iron-east-04cleardb.net'
    '/heroku_ec028af4a8b795d')
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()


# db = SQLAlchemy(app)
# app.config[
#     'SQLALCHEMY_DATABASE_URI'] = \
#     'mysql://bb3b44179051f6:d239bffa@us-cdbr-iron-east-04' \
#     '.clearnet/heroku_ec028af4a8b795d'
# app.config['SECRET_KEY'] = "NotSoSecret"
# app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# # app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
# # app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
# app.config['SQLALCHEMY_POOL_SIZE'] = 100


class Product(Base):
    __tablename__ = 'products'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', Text)
    seller_id = Column('seller_id', Integer, ForeignKey('sellers.id'))
    description1 = Column('description1', Text)
    description2 = Column('description2', Text)
    sku_id = Column('sku_id', Text)
    price = Column('price', Text)
    image_urls = Column('image_urls', Text)
    video_urls = Column('video_urls', Text)
    discount = Column('discount', Text)
    coupons = Column('coupons', Text)
    available_colors = Column('available_colors', Text)
    weight = Column('weight', Text)
    is_active = Column('is_active', Boolean, default=True)
    creation_date = Column('creation_date', DateTime)
    last_update = Column('last_update', DateTime)


class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    role_type_id = Column(Integer, ForeignKey('role_types.id'))
    username = Column('username', Text)
    password_hash = Column('password_hash', Text)
    is_active = Column('is_active', Boolean, default=True)
    creation_date = Column('creation_date', DateTime)
    last_update = Column('last_update', DateTime)

    @staticmethod
    def hash_password(password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=60 * 60):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            logger.debug("Signature expired")
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class Seller(Base):
    __tablename__ = 'sellers'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    name = Column(Text)
    contact_name = Column('contact_name', Text)
    contact_number = Column('contact_number', Text)
    email_id = Column('email_id', Text)
    is_active = Column('is_active', Boolean, default=True)
    creation_date = Column('creation_date', DateTime)
    last_update = Column('last_update', DateTime)


class RoleType(Base):
    __tablename__ = 'role_types'
    id = Column('id', Integer, primary_key=True)
    role = Column(String(100))
    is_active = Column(Boolean)
    creation_date = Column('creation_date', DateTime)
    last_update = Column('last_update', DateTime)


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    g.is_admin = False
    try:
        user = User.verify_auth_token(username_or_token)
        if not user:
            # try to authenticate with username/password
            user = session.query(User).filter_by(username=username_or_token).first()
            # user = User.query.filter_by(username=username_or_token).first()
            if not user or not user.verify_password(password):
                return False
        g.user = user
        # is user is admin, return true
        admin_role_id = session.query(RoleType).filter_by(role="ADMIN").first().id
        # admin_role_id = RoleType.query.filter_by(role="ADMIN").first().id
        if user.role_type_id == admin_role_id:
            g.is_admin = True
            return True
        seller = session.query(Seller).filter_by(user_id=user.id).first()
        # seller = Seller.query.filter_by(user_id=user.id).first()
        if not seller:
            return False
        g.seller = seller
    except SQLAlchemyError as e:
        session.rollback()
        logger.exception(e)
        raise e
    return True
