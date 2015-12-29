import unittest

import bright
from tests import settings

from bright.helpers import Forbidden, ResourceNotFound


class CollectionTests(unittest.TestCase):

    @classmethod
    def setupClass(self):
        scopes = ["collections:read", "collections:write"]
        self.bright_api = bright.Bright(client_id=settings.client_id,
                                        client_secret=settings.client_secret,
                                        scopes=scopes,
                                        **settings.kwargs
                                        )

        self.own_collections = self.bright_api.my_collections()["collections"]

    def test_get_collection(self):
        "Test we can get a collection"
        contents = ['slug', 'thumbnail_url', 'is_private', 'name', 'artworks',
                    'id', 'curator', 'description', 'draft']

        res = self.bright_api.get_collection(self.own_collections[0]["id"])
        self.assertIn("collection", res)

        for element in contents:
            self.assertIn(element, res["collection"])

    def test_update_collection(self):
        "Test we can update a collection"
        data = {
            "name": "foobar"
        }
        orig = self.bright_api.get_collection(self.own_collections[0]["id"])["collection"]
        res = self.bright_api.update_collection(orig["id"], data=data)
        self.assertEquals({}, res)

        res = self.bright_api.get_collection(self.own_collections[0]["id"])["collection"]
        self.assertEquals(data["name"], res["name"])
        self.bright_api.update_collection(orig["id"], {"name": orig["name"]})
