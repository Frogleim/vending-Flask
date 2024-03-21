#!/bin/bash

export DISPLAY=:0

# Argument 1 is the IP address
ip=$1

# Check if Firefox is already running
if ! pgrep -x "firefox" > /dev/null
then
    # Open Firefox with the Flask app URL
    firefox --new-window "http://${ip}:5000" &

    # Wait for Firefox to open and load the webpage
    sleep 5

    # Get the window ID of the Firefox window
    firefox_window_id=$(xdotool search --name "Mozilla Firefox" | head -1)

    # Send F11 key to Firefox window
    xdotool windowactivate --sync "$firefox_window_id" key "F11"
else
    echo "Firefox is already running."
fi
