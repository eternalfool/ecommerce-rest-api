from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from sqlalchemy.exc import SQLAlchemyError
import logging

app = Flask(__name__)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://bb3b44179051f6:d239bffa@us-cdbr-iron-east-04.cleardb.net/heroku_ec028af4a8b795d'
app.config['SECRET_KEY'] = "NotSoSecret"
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger = logging.getLogger(__name__)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.Text)
    seller_id = db.Column('seller_id', db.Integer, db.ForeignKey('sellers.id'))
    description1 = db.Column('description1', db.Text)
    description2 = db.Column('description2', db.Text)
    sku_id = db.Column('sku_id', db.Text)
    price = db.Column('price', db.Text)
    image_urls = db.Column('image_urls', db.Text)
    video_urls = db.Column('video_urls', db.Text)
    discount = db.Column('discount', db.Text)
    coupons = db.Column('coupons', db.Text)
    available_colors = db.Column('available_colors', db.Text)
    weight = db.Column('weight', db.Text)
    is_active = db.Column('is_active', db.Boolean, default=True)
    creation_date = db.Column('creation_date', db.DateTime)
    last_update = db.Column('last_update', db.DateTime)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    role_type_id = db.Column(db.Integer, db.ForeignKey('role_types.id'))
    username = db.Column('username', db.Text)
    password_hash = db.Column('password_hash', db.Text)
    is_active = db.Column('is_active', db.Boolean, default=True)
    creation_date = db.Column('creation_date', db.DateTime)
    last_update = db.Column('last_update', db.DateTime)

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


class Seller(db.Model):
    __tablename__ = 'sellers'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.Text)
    contact_name = db.Column('contact_name', db.Text)
    contact_number = db.Column('contact_number', db.Text)
    email_id = db.Column('email_id', db.Text)
    is_active = db.Column('is_active', db.Boolean, default=True)
    creation_date = db.Column('creation_date', db.DateTime)
    last_update = db.Column('last_update', db.DateTime)


class RoleType(db.Model):
    __tablename__ = 'role_types'
    id = db.Column('id', db.Integer, primary_key=True)
    role = db.Column(db.String(100))
    is_active = db.Column(db.Boolean)
    creation_date = db.Column('creation_date', db.DateTime)
    last_update = db.Column('last_update', db.DateTime)


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    g.is_admin = False
    try:
        user = User.verify_auth_token(username_or_token)
        if not user:
            # try to authenticate with username/password
            user = User.query.filter_by(username=username_or_token).first()
            if not user or not user.verify_password(password):
                return False
        g.user = user
        # is user is admin, return true
        admin_role_id = RoleType.query.filter_by(role="ADMIN").first().id
        if user.role_type_id == admin_role_id:
            g.is_admin = True
            return True
        seller = Seller.query.filter_by(user_id=user.id).first()
        if not seller:
            return False
        g.seller = seller
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.exception(e)
        raise e
    return True
