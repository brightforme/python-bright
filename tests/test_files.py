import unittest

import bright
from tests import settings

class FilesTests(unittest.TestCase):

    @classmethod
    def setupClass(self):
        scopes = ["artworks:read"]
        self.bright_api = bright.Bright(client_id=settings.client_id,
                                        client_secret=settings.client_secret,
                                        scopes=scopes,
                                        **settings.kwargs
                                        )

    def test_get_file(self):
        "Test we can get an artwork"
        contents = ["id", "path", "state", "codec", "quality", "size",
                    "filetype", "failure_reason", "torrent_url", "path_on_s3",
                    "path_for_frontend"]

        first_artwork = self.bright_api.my_artworks()["artworks"][0]

        res = self.bright_api.get_file(first_artwork["files"][0]["id"])
        self.assertIn("file", res)

        for element in contents:
            self.assertIn(element, res["file"])
