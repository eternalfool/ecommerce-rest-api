from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Resource, marshal_with, fields, reqparse, request
from flask import g
from models import db, auth, Product
import logging

logger = logging.getLogger(__name__)

product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'seller_id': fields.Integer,
    'description1': fields.String,
    'description2': fields.String,
    'sku_id': fields.String,
    'price': fields.String,
    'image_urls': fields.String,
    'video_urls': fields.String,
    'discount': fields.String,
    'coupons': fields.String,
    'available_colors': fields.String,
    'weight': fields.String,
    'is_active': fields.Boolean,
    'creation_date': fields.DateTime,
    'last_update': fields.DateTime
}

parser = reqparse.RequestParser()


# pagination
# parser.add_argument('limit', type=int)
# parser.add_argument('offset', type=int)

class Products(Resource):
    """
    A view of Product with CRUD operations.
    """
    @auth.login_required
    @marshal_with(product_fields, envelope='data')
    def get(self):
        """
        Gets all products of seller.
        If the id is mentioned then only get product by id.
        :return: array of products
        """
        parser.add_argument('id', type=int, location='args')
        parser.add_argument('include_inactive', type=bool, location='args')
        args = parser.parse_args()
        product_id = args['id']
        include_inactive = args['include_inactive']

        # user is Admin
        if g.is_admin:
            if product_id and include_inactive:
                products = Product.query.filter_by(id=product_id).all()
            elif product_id and not include_inactive:
                products = Product.query.filter_by(id=product_id).filter(
                    Product.is_active).all()
            elif not product_id and include_inactive:
                products = Product.query.filter(Product.is_active).all()
            else:
                # not product_id and not include_inactive:
                products = Product.query.all()
        else:  # user is not admin
            seller_id = g.seller.id
            if product_id and include_inactive:
                products = Product.query.filter_by(id=product_id).filter_by(
                    seller_id=seller_id).all()
            elif product_id and not include_inactive:
                products = Product.query.filter_by(id=product_id).filter_by(
                    seller_id=seller_id).filter(
                    Product.is_active).all()
            elif not product_id and include_inactive:
                products = Product.query.filter_by(seller_id=seller_id).all()
            else:
                # not product_id and not include_inactive
                products = Product.query.filter(Product.is_active).filter_by(
                    seller_id=seller_id).all()
        return products

    @auth.login_required
    def update_product(self, id, args):
        """
        updates product with the given params
        :param id: product_id
        :param args: params passed to update
        :return: if successful: True and product_id.
                 if failed: False and error string.
        """
        product_to_be_updated = Product.query.get(id)
        if not product_to_be_updated:
            return {"isSuccessful": False, "error": "No product with id = %s" % id}, 401
        if product_to_be_updated.seller_id != g.seller.id:
            return {"isSuccessful": False, "error": "Unauthorized access"}, 401
        for key, value in args.items():
            if value:
                setattr(product_to_be_updated, key, value)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            return {"isSuccessful": False, "error": str(e)}, 401
        finally:
             session.close()

        return {"id": id, "isSuccessful": True}, 202

    @auth.login_required
    def delete(self):
        """
        :param id: product_id
        :return: if successful: True and product_id.
                 if failed: False and error string.
        """
        parser.add_argument('id', type=int, location='args', required=True,
                            help='You must specify the product_id to delete')
        args = parser.parse_args()
        id = args['id']
        product_to_be_updated = Product.query.get(id)
        if not product_to_be_updated:
            return {"error": "No product with id = %s" % id, "isSuccessful": False}, 401
        if product_to_be_updated.seller_id != g.seller.id:
            return {"isSuccessful": False, "error": "Unauthorized access"}, 401
        product_to_be_updated.is_active = False
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            return {"error": str(e), "isSuccessful": False}, 401
        finally:
             session.close()
        return {"id": id, "isSuccessful": True}

    @auth.login_required
    def post(self):
        """
        Acts as a create_product if id is not mentioned.
        If the product_id is mention it updates the product with the given params.
        :return: if successful: True and product_id.
                 if failed: False and error string.
        """
        logger.debug(request.data)
        parser.add_argument('id', type=int, location='json')
        parser.add_argument('name', type=str, location='json')
        parser.add_argument('description1', type=str, location='json')
        parser.add_argument('description2', type=str, location='json')
        parser.add_argument('sku_id', type=str, location='json')
        parser.add_argument('price', type=str, location='json')
        parser.add_argument('image_urls', type=str, location='json')
        parser.add_argument('video_urls', type=str, location='json')
        parser.add_argument('discount', type=str, location='json')
        parser.add_argument('coupons', type=str, location='json')
        parser.add_argument('available_colors', type=str, location='json')
        parser.add_argument('weight', type=str, location='json')
        args = parser.parse_args()
        args['seller_id'] = g.seller.id
        id = args['id']
        if id:
            return self.update_product(id, args)
        else:
            return self.create_product(args)

    def create_product(self, args):
        """
            creates product with the given params
            :param args: params passed to update
            :return: if successful: True and product_id.
                     if failed: False and error string.
        """
        if args['name'] is None:
            return {"isSuccessful": False, "error": "You must specify the name"}, 401
        product = Product(name=args['name'], seller_id=args['seller_id'],
                          description1=args['description1'],
                          description2=args['description2'], sku_id=args['sku_id'],
                          price=args['price'],
                          image_urls=args['image_urls'], video_urls=args['video_urls'],
                          discount=args['discount'],
                          coupons=args['coupons'],
                          available_colors=args['available_colors'],
                          weight=args['weight'])
        try:
            db.session.add(product)
            db.session.commit()
            return {"id": product.id, "isSuccessful": True}, 202
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            return {"error": str(e), "isSuccessful": False}, 401
        finally:
             session.close()
