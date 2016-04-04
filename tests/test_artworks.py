import unittest

import bright
from tests import settings

from bright.helpers import Forbidden, ResourceNotFound


class ArtworkTests(unittest.TestCase):

    @classmethod
    def setupClass(self):
        scopes = ["artworks:read", "artworks:write"]
        self.bright_api = bright.Bright(client_id=settings.client_id,
                                        client_secret=settings.client_secret,
                                        scopes=scopes,
                                        **settings.kwargs
                                        )

        self.own_artworks = self.bright_api.my_artworks()["artworks"]

    def test_get_artwork(self):
        "Test we can get an artwork"
        contents = ['slug', 'thumbnail_url', 'name', 'tags', 'is_private',
                    'collections', 'id', 'short_description', 'description',
                    'files']

        res = self.bright_api.get_artwork(self.own_artworks[0]["id"])
        self.assertIn("artwork", res)

        for element in contents:
            self.assertIn(element, res["artwork"])

    def test_get_all_artworks(self):
        "Test we can get all artworks"
        contents = ['slug', 'thumbnail_url', 'name', 'tags', 'is_private',
                    'collections', 'id', 'short_description', 'description',
                    'files']

        res = self.bright_api.get_all_artworks()

        self.assertIn("pages", res)
        self.assertIn("artworks", res)

        for artwork in res["artworks"]:
            for element in contents:
                self.assertIn(element, artwork)

    def test_update_artwork(self):
        "Test we can update an artwork"
        data = {
            "name": "foobar",
            "tags": ["none"]
        }
        orig = self.bright_api.get_artwork(self.own_artworks[0]["id"])["artwork"]
        res = self.bright_api.update_artwork(orig["id"], data=data)

        self.assertEquals(data["name"], res["artwork"]["name"])
        self.bright_api.update_artwork(orig["id"], {"name": orig["name"]})

    def test_like_artwork(self):
        "Test that we can like an artwork"
        # TODO
        pass

    def test_unlike_artwork(self):
        "Test that we can unlike an artwork"
        # TODO
        pass

    def test_flow(self):
        "Test that we can get our personalized flow"
        contents = ["artworks", "oldest"]
        res = self.bright_api.get_flow()

        for element in contents:
            self.assertIn(element, res)
