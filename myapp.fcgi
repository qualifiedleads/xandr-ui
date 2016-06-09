#!/usr/bin/python2.7
from flup.server.fcgi import WSGIServer
from api import app


if __name__ == '__main__':
    WSGIServer(app, bindAddress='/run/shm/caravel.sock').run()
