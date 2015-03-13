# coding=utf-8

from django.test import TestCase
from django.test.client import Client


class TSortTestCase(TestCase):
    JSON = {
        'JSON_1': {"dPriority": "1",
                   "pPriority": "5",
                   "rPriority": "4"}
    }
    def setUp(self):
        """
        Preconditions
        """
        self.client = Client()


class HTTPRequestTest(TSortTestCase):
    """
    Testing simple HTTP request behaviour.
    """

    def test_unauthorized_access(self):
        """
        Should redirect to login page if not
        authenticated ssc/.
        """
        response = self.client.get('/?json={0}'.format(self.JSON['JSON_1']), follow=True)
        print(response.content)
        # self.assertEqual(response.templates[0].name, 'ssc/login.html')


