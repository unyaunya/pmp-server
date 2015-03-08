#! python3
# -*- coding: utf-8 -*-

from pmpserver import app

if __name__ == '__main__':
    host='0.0.0.0'
    port = 5000 #未使用
    app.debug = True
    app.run(host=host)
