#!/bin/bash

systemctl disable new-uwsgi
systemctl stop new-uwsgi

echo "del systemd service success!"

