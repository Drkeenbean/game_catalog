#!/usr/bin/python
from app import app

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'Eo4_NLu6jAU0UnPiqrjEdLJG'
    app.run(host='0.0.0.0', port=5000)
