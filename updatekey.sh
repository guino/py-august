#!/bin/bash

cd /home/pi/py-august
KEY=$(python getkey.py)

echo '{ "offlineKey": "'$KEY'", "offlineKeyOffset": 1 , "address": "0.0.0.0" }' > /home/pi/augustctl/config.json

sudo systemctl restart august
