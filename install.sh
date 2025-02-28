#!/bin/bash

set -e  # Stop on any error

echo "Starting installation..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-venv python3-pip cups cups-pdf git poppler-utils

# Enable and start CUPS service
sudo systemctl enable cups
sudo systemctl start cups

# Allow remote access to CUPS
sudo cupsctl --remote-any
sudo systemctl restart cups

# Create printer queue
lpadmin -p Pi_Printer -E -v cups-pdf:/ -m everywhere

# Create project folder
mkdir -p ~/label_printer
cd ~/label_printer

# Clone GitHub repo
git clone https://github.com/YourUsername/raspi-label-printer.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Copy systemd service file
sudo cp label_printer.service /etc/systemd/system/label_printer.service

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable label_printer
sudo systemctl start label_printer

echo "Installation completed successfully! The Raspberry Pi is now acting as a Wi-Fi printer."
