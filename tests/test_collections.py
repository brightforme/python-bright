import unittest

import bright
from tests import settings

from bright.helpers import Forbidden, ResourceNotFound


class CollectionTests(unittest.TestCase):

    @classmethod
    def setupClass(self):
        scopes = ["collections:read", "collections:write", "collections:like",
                  "artworks:read", "user:read"]
        self.bright_api = bright.Bright(client_id=settings.client_id,
                                        client_secret=settings.client_secret,
                                        scopes=scopes,
                                        **settings.kwargs
                                        )

        self.own_collections = self.bright_api.my_collections()["collections"]
        self.own_artworks = self.bright_api.my_artworks()["artworks"]

    def test_get_collection(self):
        "Test we can get a collection"
        contents = ['slug', 'thumbnail_url', 'is_private', 'name', 'artworks',
                    'id', 'curator', 'description', 'draft']

        res = self.bright_api.get_collection(self.own_collections[0]["id"])
        self.assertIn("collection", res)

        for element in contents:
            self.assertIn(element, res["collection"])

    def test_get_all_collections(self):
        "Test we can get all collections"
        contents = ['slug', 'thumbnail_url', 'is_private', 'name', 'artworks',
                    'id', 'curator', 'description', 'draft']

        res = self.bright_api.get_all_collections()

        self.assertIn("pages", res)
        self.assertIn("collections", res)

        for collection in res["collections"]:
            for element in contents:
                self.assertIn(element, collection)

    def test_create_collection(self):
        "Test we can create a collection"
        contents = ['slug', 'thumbnail_url', 'is_private', 'name', 'artworks',
                    'id', 'curator', 'description', 'draft']
        res = self.bright_api.create_collection("test", "'tis but a test", False)
        
        for element in contents:
            self.assertIn(element, res["collection"])

        self.bright_api.delete_collection(res["collection"]["id"])

    def test_delete_collection(self):
        "Test we can delete a collection"
        res = self.bright_api.create_collection("test", "'tis but a test", False)["collection"]
        me = self.bright_api.my_collections()["collections"]

        self.assertIn(res, me)
        
        self.bright_api.delete_collection(res["id"])
        me = self.bright_api.my_collections()["collections"]

        self.assertNotIn(res, me)

    def test_update_collection(self):
        "Test we can update a collection"
        data = {
            "name": "foobar"
        }
        orig = self.bright_api.get_collection(self.own_collections[0]["id"])["collection"]
        res = self.bright_api.update_collection(orig["id"], data=data)["collection"]
        self.assertEquals(data["name"], res["name"])
        self.bright_api.update_collection(orig["id"], {"name": orig["name"]})

    def test_add_to_collection(self):
        "Test we can add artworks to collections"
        collec = self.own_collections[0]
        artworks_not_in_collec = [x for x in self.own_artworks
                                  if x in collec["artworks"]]
        artwork_id = artworks_not_in_collec[0]["id"]

        res = self.bright_api.add_to_collection(collec["id"], artwork_id)
        self.assertEquals({}, res)

        res = self.bright_api.get_collection(collec["id"])
        self.assertIn(artwork_id, res["collection"]["artworks"])

        self.bright_api.remove_from_collection(collec["id"], artwork_id)

    def remove_from_collection(self):
        "Test we can remove artworks from collections"
        collec = self.own_collections[0]
        artworks_in_collec = [x for x in self.own_artworks
                              if x in collec["artworks"]]
        artwork_id = artworks_in_collec[0]["id"]

        res = self.bright_api.remove_from_collection(collec["id"], artwork_id)
        self.assertEquals({}, res)

        res = self.bright_api.get_collection(collec["id"])
        self.assertNotIn(artwork_id, res["collection"]["artworks"])

        self.bright_api.add_to_collection(collec["id"], artwork_id)

    def test_like_collection(self):
        "Test that we can like a collection"
        own_id = self.bright_api.me()["user"]["id"]
        all_collec = self.bright_api.get_all_collections()["collections"]
        collec = list(filter(lambda c: not own_id in c["likes"], all_collec))[0]

        res = self.bright_api.like_collection(collec["id"])
        self.assertEquals({}, res)

        res = self.bright_api.get_collection(collec["id"])
        self.assertIn(own_id, res["collections"]["likes"])

        self.bright_api.unlike_collection(collec["id"])

    def test_unlike_collection(self):
        "Test that we can unlike a collection"
        own_id = self.bright_api.me()["user"]["id"]
        all_collec = self.bright_api.get_all_collections()["collections"]
        collec = list(filter(lambda c: not own_id in c["likes"], all_collec))[0]

        _ = self.bright_api.like_collection(collec["id"])
        res = self.bright_api.unlike_collection(collec["id"])
        self.assertEquals({}, res)

        res = self.bright_api.get_collection(collec["id"])
        self.assertNotIn(own_id, res["collections"]["likes"])

        self.bright_api.like_collection(collec["id"])
