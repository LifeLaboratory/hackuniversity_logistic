import unittest
import requests as req
from api.helpers import base_name as names


class TestStringMethods(unittest.TestCase):
    def test_auth(self):
        s = req.Session()
        data = {
            names.LOGIN: 'ralden',
            names.PASSWORD: 'ralden'
        }
        r = s.get('http://127.0.0.1:13451/auth', data=data)
        #result = Gis.converter(r.text)
        #self.assertTrue(result.get(names.SESSION, None), None)
        return
