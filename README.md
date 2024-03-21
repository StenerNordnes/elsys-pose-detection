python3 -m venv --system-site-packages env



# Dette er i utganspunktet ikke nødvendig om pakkene som kreves allerede er installert
sudo apt update && sudo apt upgrade
sudo apt install libcap-dev libatlas-base-dev ffmpeg libopenjp2-7
sudo apt install libcamera-dev
sudo apt install libkms++-dev libfmt-dev libdrm-dev


pip install --upgrade pip
pip install wheel
pip install rpi-libcamera rpi-kms picamera2