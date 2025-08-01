#!/bin/bash

echo "Installing dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-dev libudev-dev
pip3 install -r requirements.txt

echo "Setting up uinput permissions..."
sudo modprobe uinput
sudo chmod 666 /dev/uinput

echo "Done."
