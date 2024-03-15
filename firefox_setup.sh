#!/bin/bash

export DISPLAY=:0


# Argument 1 is the IP address
ip=$1

# Open Firefox with the Flask app URL
firefox --new-window  "http://${ip}:5000"
sleep 5
xdotool search --name "Mozilla Firefox" key "F11"

