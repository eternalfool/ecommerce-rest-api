import sys

sys.path.append('..')
from flask_testing import TestCase
import unittest
from run import app
from models.models import Product
import json
import time
from common.utils import get_auth_headers
import logging

logger = logging.getLogger(__name__)
logging.basicConfig()

lifebuoy_details = {
    'name': "Lifebouy",
    'description1': "Tandarusti ki raksha karta hai lifebouy",
    'description2': "Lifebouy hai jahan tandarusti hai wahan",
    'sku_id': "SKU-86e467-UKS",
    'price': "99.95",
    'image_urls': "['http://www.lifebuoy.co.za/Resources/Images/logo.gif']",
    'video_urls': "['https://www.youtube.com/watch?v=VsnP_6kdtDY', "
                  "'https://www.youtube.com/watch?v=AOU3ZIrUiVM']",
    'discount': "7.50",
    'coupons': "['WNG50', 'FP40']",
    'available_colors': "['RED', '0x454']",
    'weight': "45.76 gms",
}

dettol_details = {
    'name': "Dettol",
    'description1': "Dettol Dettol Dettol Dettol",
    'description2': "Dettol Dettol Dettol Dettol Ho",
    'sku_id': "SKU-96ghi7-UKS",
    'price': "95.95",
    'image_urls': "['http://www.dettol.co.in/media/1463092/Dettol-original-Soap"
                  "-Packshot-300-X-600.jpg']",
    'video_urls': "['https://www.youtube.com/watch?v=iiGAPr9Vl0U']",
    'discount': "5.50",
    'coupons': "['DD50', 'FP40']",
    'available_colors': "['BLUE', '0x454']",
    'weight': "75.46 gms",
}


def get_product(details):
    product = Product()
    for key, value in details.items():
        if value:
            setattr(product, key, value)
    return product


class TestProducts(TestCase):
    """Test Suite for CRUD operation of products"""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def create_user_and_token(self, username, password):
        """
        First creates a user and then generates a user token.
        The token is then saved to be used for testing
        :param username: username
        :param password: password
        """
        seller_params = dict(username=username, password=password,
                             name="Amazon", contact_name="Jeff Bezos",
                             contact_number="8975217919", email_id="bezos@amazon.com")
        logger.info("Setting up user and token")
        self.client.post('/sellers', data=json.dumps(seller_params),
                         content_type='application/json')
        headers = get_auth_headers(username, password)
        token = json.loads(self.client.get('/token', headers=headers).data)["token"]
        logger.info("token = %s" % token)
        headers = get_auth_headers(token, None)
        self.headers = headers

    def setUp(self):
        """
        Instantiates a user for testing.
        """
        unique_username = "username%s" % int(time.time())
        password = "dadada"
        self.create_user_and_token(unique_username, password)

    def test_crud_operations(self):
        """
        - create a product
        - fetch it
        - update it
        - delete it
        """
        # Create Product
        dettol = get_product(dettol_details)
        resp = self.client.post('/products', data=json.dumps(dettol_details),
                                content_type='application/json', headers=self.headers)
        dettol_id = json.loads(resp.data)['id']
        self.assertEquals(resp.status_code, 202)

        # Gets product
        dettol_id_dict = {"id": dettol_id}
        dettol_get_resp = self.client.get('/products', query_string=dettol_id_dict,
                                          headers=self.headers)
        self.assertEquals(dettol_get_resp.status_code, 200)
        dettol_get_product = Product()
        dettol_data = json.loads(dettol_get_resp.data)['data'][0]
        for key, value in dettol_data.items():
            setattr(dettol_get_product, key, value)
        self.assertEquals(self.check_for_equality(dettol, dettol_get_product), True)

        # update product
        lifebuoy_details['id'] = dettol_id
        resp = self.client.post('/products', data=json.dumps(lifebuoy_details),
                                content_type='application/json', headers=self.headers)
        self.assertEquals(resp.status_code, 202)
        lifebuoy_id = json.loads(resp.data)['id']
        self.assertEquals(dettol_id, lifebuoy_id)
        lifebuoy = get_product(lifebuoy_details)
        lifebuoy.id = dettol_id
        get_lifebuoy = Product.query.get(lifebuoy_id)
        self.assertEquals(self.check_for_equality(lifebuoy, get_lifebuoy), True)

        # delete product
        self.client.delete('/products', query_string=dettol_id_dict,
                           headers=self.headers)
        pass

    @staticmethod
    def check_for_equality(product1, product2):
        return product1.name == product2.name and \
               product1.description1 == product2.description1 and \
               product1.description2 == product2.description2 and \
               product1.sku_id == product2.sku_id and \
               product1.price == product2.price and \
               product1.image_urls == product2.image_urls and \
               product1.video_urls == product2.video_urls and \
               product1.discount == product2.discount and \
               product1.coupons == product2.coupons and \
               product1.available_colors == product2.available_colors and \
               product1.weight == product2.weight

    def tearDown(self):
        pass

# runs the unit tests in the module
if __name__ == '__main__':
  unittest.main()

