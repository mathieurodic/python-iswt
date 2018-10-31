#!/usr/bin/env python3

from common.wsgi import app as application

if __name__ == '__main__':
    application.run(threaded=True)
