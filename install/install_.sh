#!/bin/bash

DIR="$( cd "$( dirname "$0"  )" && pwd  )"
cp $DIR/new-uwsgi.service /lib/systemd/system
systemctl enable new-uwsgi
systemctl restart new-uwsgi

echo "add systemd service success!"
