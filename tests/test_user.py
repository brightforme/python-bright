import unittest

import bright
import settings

bright_api = bright.Bright(client_id=settings.client_id,
                           client_secret=settings.client_secret,
                           **settings.kwargs)

def test_get_me():
    "Test we can get our own profile"
    contents = ["cover_url", "picture_url", "fullname", "screenname", "bio",
                "accounts", "user_type", "counts"]
    res = bright_api.me()
    unittest.assertIn(res, "user")

    for element in contents:
        unittest.assertIn(res["user"], element)

def test_get_user():
    "Test that we can get another users profile"
    contents = ["cover_url", "picture_url", "fullname", "screenname", "bio",
                "accounts", "user_type", "counts"]
    res = bright_api.get_user("test_user")
    unittest.assertIn(res, "user")

    for element in contents:
        unittest.assertIn(res["user"], element)

def test_get_user_404():
    "test that we get an exception if the user does not exist"
    with unittest.assertRaises(bright.ResourceNotFound):
        res = bright_api.get_user("this_user_does_not_exist")
