# coding: utf-8

from __future__ import absolute_import

from swagger_server.models.info import Info
from . import BaseTestCase
from six import BytesIO
from flask import json


class TestDefaultController(BaseTestCase):
    """ DefaultController integration test stubs """

    def test_fingerprint_get(self):
        """
        Test case for fingerprint_get

        
        """
        query_string = [('music_buffer', 'music_buffer_example')]
        response = self.client.open('/team2/fingerprint',
                                    method='GET',
                                    content_type='application/json',
                                    query_string=query_string)
        self.assert200(response, "Response body is : " + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
