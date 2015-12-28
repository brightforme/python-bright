import unittest

import bright
import settings

from bright.helpers import Forbidden, ResourceNotFound


class UserTests(unittest.TestCase):

    @classmethod
    def setupClass(self):
        self.bright_api = bright.Bright(client_id=settings.client_id,
                                        client_secret=settings.client_secret,
                                        **settings.kwargs)

    def test_get_me(self):
        "Test we can get our own profile"
        contents = ["cover_url", "picture_url", "fullname", "screenname", "bio",
                    "accounts", "user_type", "counts"]
        res = self.bright_api.me()
        self.assertIn("user", res)

        for element in contents:
            self.assertIn(element, res["user"])

    def test_get_user(self):
        "Test that we can get another users profile"
        contents = ["cover_url", "picture_url", "fullname", "screenname", "bio",
                    "accounts", "user_type", "counts"]
        res = self.bright_api.get_user("test_user")
        self.assertIn("user", res)

        for element in contents:
            self.assertIn(element, res["user"])

    def test_get_user_404(self):
        "Test that we get an exception if the user does not exist"
        with self.assertRaises(ResourceNotFound):
            res = self.bright_api.get_user("this_user_does_not_exist")

    def test_update_me(self):
        "Tes that we can update ourselves"
        data = {
          "user": {
            "screenname": "foobar"
          }
        }
        res = self.bright_api.update_me(data)
        self.assertIn("user", res)
        self.assertIn("screenname", res["user"])
        self.assertEquals(data["screenname"], res["user"]["screenname"])
