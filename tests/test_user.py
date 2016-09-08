import unittest

import bright
from tests import settings

from bright.helpers import Forbidden, ResourceNotFound


class UserTests(unittest.TestCase):

    @classmethod
    def setupClass(self):
        scopes = ["user:read", "user:write", "user:follow", "artworks:read",
                  "collections:read"]
        self.bright_api = bright.Bright(client_id=settings.client_id,
                                        client_secret=settings.client_secret,
                                        scopes=scopes,
                                        **settings.kwargs
                                        )

    def test_get_me(self):
        "Test we can get our own profile"
        contents = ["picture_url", "fullname", "screenname", "bio",
                    "accounts", "user_type", "accounts", "artworks", "collections"]
        res = self.bright_api.me()
        self.assertIn("user", res)

        for element in contents:
            self.assertIn(element, res["user"])

    def test_get_user(self):
        "Test that we can get another users profile"
        contents = ["picture_url", "fullname", "screenname", "bio",
                    "accounts", "user_type"]
        res = self.bright_api.get_user("testuser")
        self.assertIn("user", res)

        for element in contents:
            self.assertIn(element, res["user"])

    def test_get_user_404(self):
        "Test that we get an exception if the user does not exist"
        with self.assertRaises(ResourceNotFound):
            res = self.bright_api.get_user("this_user_does_not_exist")

    def test_update_me(self):
        "Test that we can update ourselves"
        data = {
          "screenname": "foobar"
        }
        orig = self.bright_api.me()
        res = self.bright_api.update_me(data)
        self.assertEquals(res, {})
        res = self.bright_api.me()
        self.assertIn("user", res)
        self.assertIn("screenname", res["user"])
        self.assertEquals(data["screenname"], res["user"]["screenname"])
        self.bright_api.update_me({"screenname": orig["user"]["screenname"]})

    def test_my_notifications(self):
        "Test that we can get our own notifications"
        res = self.bright_api.my_notifications()
        self.assertIn("notifications", res)
        self.assertIn("read", res["notifications"])
        self.assertIn("unread", res["notifications"])

    def test_my_artworks(self):
        "Test that we can get our own artworks"
        res = self.bright_api.my_artworks()
        self.assertIn("artworks", res)
        self.assertIn("pages", res)

    def test_my_collections(self):
        "Test that we can get our own artworks"
        res = self.bright_api.my_collections()
        self.assertIn("collections", res)
        self.assertIn("pages", res)

    # Follow/Unfollow are interdependent. Urgh.
    def test_follow(self):
        "Test that we can follow a user"
        own_id = self.bright_api.me()["user"]["id"]
        uid = self.bright_api.get_user("testuser")["user"]["id"]

        res = self.bright_api.follow_user(uid)
        self.assertEquals({}, res)

        user = self.bright_api.get_user("testuser")["user"]
        self.assertIn(own_id, [x["id"] for x in user["followers"]])

        self.bright_api.unfollow_user(uid)

    def test_unfollow(self):
        "Test that we can unfollow a user"
        own_id = self.bright_api.me()["user"]["id"]
        uid = self.bright_api.get_user("testuser")["user"]["id"]

        try:
            self.bright_api.follow_user(uid)
        except:
            pass

        user = self.bright_api.get_user("testuser")["user"]
        self.assertIn(own_id, [x["id"] for x in user["followers"]])

        res = self.bright_api.unfollow_user(uid)
        self.assertEquals({}, res)

        user = self.bright_api.get_user("testuser")["user"]
        self.assertNotIn(own_id, [x["id"] for x in user["followers"]])
