import logging

from flask import g
from flask_restful import Resource, marshal_with, fields, reqparse
from sqlalchemy.exc import SQLAlchemyError

from models.models import Seller, User, auth, db

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
    """
    A view of Seller with CRUD operations.
    """
    @auth.login_required
    @marshal_with(output_fields)
    def get(self):
        """
        Get seller info
        """
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

    def post(self):
        """
        Create or update an existing seller.
        Update if triggered if the seller_id is passed.
        """
        logger.debug("in post of create seller")
        logger.debug("info : in post of create seller")
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
        finally:
             db.session.close()

    @auth.login_required
    def update_seller(self, id, args):
        try:
            seller = Seller.query.get(id)
            if not seller:
                return {"error": "No seller with id = %s" % id,
                        "isSuccessful": False}, 401
            # If a seller is trying to update another seller
            if id != g.seller.id and not g.is_admin:
                return {"error": "you don't have permission to update this seller"
                        , "isSuccessful": False}, 401
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
        finally:
             db.session.close()
