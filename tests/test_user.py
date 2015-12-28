import unittest

import bright
import settings

bright_api = bright.Bright(client_id=settings.client_id,
                           client_secret=settings.client_secret,
                           **settings.kwargs)

def test_get_me():
    "Test we can get a user"
    contents = ["cover_url", "picture_url", "fullname", "screenname", "bio",
                "accounts", "user_type", "counts"]
    res = bright_api.me()
    unittest.assertIn(res, "user")

    for element in contents:
        unittest.assertIn(res["user"], element)
