#!/usr/bin/env python3
from api import create_app
from os import getenv

app = create_app(getenv('CONFIG') or 'testing')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
