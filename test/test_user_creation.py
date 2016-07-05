#!/usr/bin/env python

import sys

sys.path.append('..')
from flask_testing import TestCase
from run import app
from models.models import Seller
import json
import time
from common.utils import get_auth_headers
import unittest



class TestSeller(TestCase):
    """Test Suite for creation of user and fetching it's token."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        pass

    def test_create_seller_and_fetch_token(self):
        """
        Creates a seller and fetches it's api token.
        """

        username, password = ("username%s" % int(time.time()), "dadada")
        seller_params = dict(username=username, password=password,
                             name="brotherNero", contact_name="Matt Hardy",
                             contact_number="619", email_id="Jeff Hardy")
        response = self.client.post(
            '/sellers', data=json.dumps(seller_params), content_type='application/json')
        self.assertEqual(response.status_code, 202)
        data = json.loads(response.data)
        seller_id = data["id"]
        seller = Seller.query.get(seller_id)
        self.assertIsNotNone(seller)
        self.assertEquals(seller.name, "brotherNero")
        self.assertEquals(seller.contact_name, "Matt Hardy")
        self.assertEquals(seller.contact_number, "619")
        self.assertEquals(seller.email_id, "Jeff Hardy")
        headers = get_auth_headers(username, password)

        # get token
        token_response = self.client.get('/token', headers=headers)
        print token_response
        print token_response.data
        self.assertEqual(token_response.status_code, 200)
        data = json.loads(token_response.data)
        token = data["token"]
        self.assertIsNotNone(token)

    def tearDown(self):
        pass
        # db.session.remove()
        # db.drop_all()

# runs the unit tests in the module
if __name__ == '__main__':
  unittest.main()
