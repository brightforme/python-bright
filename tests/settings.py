import os
import json

client_id = os.getenv("BRIGHT_CLIENT_ID")
client_secret = os.getenv("BRIGHT_CLIENT_SECRET")
kwargs = os.getenv("BRIGHT_KWARGS", {})
if kwargs:
    kwargs = json.loads(kwargs)

try:
    from tests.local_settings import *
except ImportError:
    pass
