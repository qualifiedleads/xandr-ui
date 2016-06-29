#!/bin/bash
uwsgi --chdir=. \
    --module=config.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=config.settings \
    --master --pidfile=/tmp/rtb-project.pid \
    --socket=/var/run/rtb_socket \  # can also be IP:port
    --processes=5 \                 # number of worker processes
    --uid=1000 --gid=2000 \         # if root, uwsgi can drop privileges
    --harakiri=20 \                 # respawn processes taking more than 20 seconds
    --max-requests=5000 \           # respawn processes after serving 5000 requests
    --vacuum \                      # clear environment on exit
#    --home=/path/to/virtual/env \   # optional path to a virtualenv
    --daemonize=/var/log/uwsgi/rtb-project.log