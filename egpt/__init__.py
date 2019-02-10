import os


__name__="egpt"
__version__="0.1"

RDB_URL='http://localhost:12345'
if 'RDB_URL' in os.environ:
    RDB_URL=os.environ["RDB_URL"]
