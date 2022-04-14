from factories.factories import OrguserFactory, ProjectFactory, TeamFactory
import unittest

import os
import sys
from dotenv import load_dotenv


PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from resources import ooti # noqa E402

# Loading environment variables (stored in .env file)
load_dotenv()

OOTI_AUTH = os.getenv("OOTI_AUTH")
OOTI_PASSWORD = os.getenv("OOTI_PASSWORD")

sdk = ooti.OotiAPI(OOTI_AUTH, OOTI_PASSWORD)
sdk.connect()

""" Not cleanup yet
class TestImports(unittest.TestCase):
    def test_get_imports_count(self):
        response = sdk.Settings.get_imports_count()
        self.assertEqual(response['status'], 200)

    def test_get_exports_list(self):
        response = sdk.Settings.get_exports_list()
        self.assertEqual(response['status'], 200)

    def test_create_export(self):
        payload = {
            "orguser": 5042,
            "team": 1689,
            "project": 11702,
            "items": 0,
            "include_documents": True
        }
        response = sdk.Settings.create_export(payload)
        print(response)
        self.assertEqual(response['status'], 201)

    def test_get_export_details(self):
        response = sdk.Settings.get_export_details(16)
        self.assertEqual(response['status'], 200)

    def test_delete_export(self):
        response = sdk.Settings.delete_export(15)

    def test_get_import_list(self):
        response = sdk.Settings.get_imports_list()
        self.assertEqual(response['status'], 200)

    def test_create_import(self):
        payload = {
            "data": {}
        }
        response = sdk.Settings.create_import(payload)
        self.assertEqual(response['status'], 201)

    def test_get_import_details(self):
        response = sdk.Settings.get_import_details(66)
        self.assertEqual(response['status'], 200)

    def test_update_import_list(self):
        payload = {
            "status": 3,
            "type": 6
        }
        response = sdk.Settings.update_import_details(66, payload)
        self.assertEqual(response['status'], 200)

    def test_delete_import(self):
        response = sdk.Settings.delete_import(71)
"""

if __name__ == '__main__':
    unittest.main()