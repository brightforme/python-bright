# python-bright

Official Bright API wrapper

## Installation

Method with pip: if you have pip installed, just type this in a terminal (sudo is optional on some systems)

```
(sudo) pip install python-bright
```

Method by hand: download the sources, either on PyPI or (if you want the development version) on Github, unzip everything in one folder, open a terminal and type

```
(sudo) python setup.py install
```


## Usage

### User Credentials Flow

```
from bright import Bright
api = Bright(client_id=YOUR_CLIENT_ID,
			username='john@example.com',
			password='johnpassword'
)
print(api.me())
```

