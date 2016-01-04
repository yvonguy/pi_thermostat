#!/usr/bin/python
from therm.app import app

#quit = True
#while quit != False:
try:
    app.run(host='0.0.0.0',port=80,debug=True)
except (KeyboardInterrupt, SystemExit):
    exit(0)
#        quit = True

