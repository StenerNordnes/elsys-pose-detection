## Pose Me In - Posedeteksjon

### Installasjon - Linux

1. Klon prosjektet fra github
2. Installer nødvendige pakker

    Kjør følgende kommandoer i terminalen:

    ```bash
    sudo apt update && sudo apt upgrade
    sudo apt install libcap-dev libatlas-base-dev ffmpeg libopenjp2-7
    sudo apt install libcamera-dev
    sudo apt install libkms++-dev libfmt-dev libdrm-dev


    pip install --upgrade pip
    pip install wheel
    pip install rpi-libcamera rpi-kms picamera2

    ```

3. Initialiser et Python virtual environment

```bash
python3 -m venv --system-site-packages .venv
```

4. Aktiver virtual environment

```bash
source .venv/bin/activate
```

5. Installer nødvendige pakker

```bash
pip install tensorflow tensorflow_hub matplotlib adafruit-blinka adafruit-circuitpython-neopixel tqdm scikit-learn
```

6. Kjør programmet

```bash
python3 main.py
```


















<!-- # Dette er i utganspunktet ikke nødvendig om pakkene som kreves allerede er installert -->




