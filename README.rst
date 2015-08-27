python-bright
=============

Official Bright API wrapper

Installation
------------

Method with pip: if you have pip installed, just type this in a terminal
(sudo is optional on some systems)

::

    pip install python-bright

Method by hand: download the sources, either on PyPI or (if you want the
development version) on Github, unzip everything in one folder, open a
terminal and type

::

    python setup.py install

Usage
-----

All OAuth2 authorization flows supported by the BRIGHT API are available
in python-bright.

Basic Flow
~~~~~~~~~~

If you only need read-only access to public resources, simply provide a
client\_id and client\_secret:

.. code:: python

    from bright import Bright
    api = Bright(client_id=YOUR_CLIENT_ID,
                client_secret=YOUR_CLIENT_SECRET
    )
    print(api.get_all_artworks())

User Credentials Flow
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from bright import Bright
    api = Bright(client_id=YOUR_CLIENT_ID,
                username='john@example.com',
                password='johnpassword'
    )
    print(api.me())