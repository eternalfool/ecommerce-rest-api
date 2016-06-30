from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Api
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Api
from flask_restful import Resource, marshal_with, fields, reqparse
import traceback
from flask import abort, jsonify, make_response, request
from models import db
from models import Seller, User, auth
import json
import logging

output_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'contact_name': fields.String,
    'contact_number': fields.String,
    'email_id': fields.String,
    'is_active': fields.Boolean,
    'creation_date': fields.DateTime,
    'last_update': fields.DateTime,
}
logger = logging.getLogger(__name__)

parser = reqparse.RequestParser()


class Sellers(Resource):
    @auth.login_required
    @marshal_with(output_fields)
    def get(self):
        parser.add_argument('id', type=int, location='args')
        parser.add_argument('include_inactive', type=bool, location='args')
        args = parser.parse_args()
        id = args['id']
        include_inactive = args['include_inactive']
        if id and include_inactive:
            sellers = Seller.query.filter_by(id=id).all()
        elif id and not include_inactive:
            sellers = Seller.query.filter_by(id=id).filter(Seller.is_active).all()
        elif not id and include_inactive:
            sellers = Seller.query.all()
        else:
            sellers = Seller.query.filter(Seller.is_active).all()
        return sellers

    def delete(self):
        parser.add_argument('id', type=int, location='json', required=True,
                            help='You must specify the product_id to delete')
        args = parser.parse_args()
        id = args['id']
        product_to_be_updated = Seller.query.get(id)
        if not product_to_be_updated:
            return {"error": "No product with id = %s" % id, "isSuccessful": False}, 401
        product_to_be_updated.is_active = False
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception("Error while deleting")
            return {"error": str(e), "isSuccessful": False}, 401
        return {"isSuccessful": True}

    def post(self):
        print "In seller post"
        parser.add_argument('id', type=int, location='json')
        parser.add_argument('name', type=str, location='json')
        parser.add_argument('contact_name', type=str, location='json')
        parser.add_argument('contact_number', type=str, location='json')
        parser.add_argument('email_id', type=str, location='json')
        parser.add_argument('username', type=str, location='json')
        parser.add_argument('password', type=str, location='json')
        args = parser.parse_args()
        id = args['id']
        if id:
            return self.update_seller(id, args)
        else:
            return self.create_seller(args)

    def create_seller(self, args):
        try:
            user = User(role_type_id=1, username=args['username'],
                        password_hash=User.hash_password(args['password']))
            db.session.add(user)
            db.session.commit()
            seller = Seller(user_id=user.id, name=args['name'],
                            contact_name=args['contact_name'],
                            contact_number=args['contact_number'],
                            email_id=args['email_id'])
            db.session.add(seller)
            db.session.commit()
            return {"id": seller.id, "isSuccessful": True}, 202
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception("Error while creating seller")
            return {"error": str(e), "isSuccessful": False}, 401

    def update_seller(self, id, args):
        try:
            seller = Seller.query.get(id)
            if not seller:
                return {"error": "No product with id = %s" % id,
                        "isSuccessful": False}, 401
            for key, value in args.items():
                if value:
                    setattr(seller, key, value)
            db.session.add(seller)
            db.session.commit()
            return {"id": seller.id, "isSuccessful": True}, 202
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception("Error while updating seller")
            return {"error": str(e), "isSuccessful": False}, 401