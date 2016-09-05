#!venv/bin/python
import sys

from api import app

port = 8080
if len(sys.argv) > 1:
    try:
        port = int(sys.argv[1]) 
    except:
        pass

app.run('0.0.0.0', port=port)
