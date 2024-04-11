
import time
import board
import neopixel
import RPi.GPIO as GPIO


import time
import board
import neopixel


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 30

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# GPIO pin numbers for the signals
SIGNAL_PIN_1 = 22
SIGNAL_PIN_2 = 24
SIGNAL_PIN_3 = 26

BUTTON_PIN = 15

# Number of LED lights
NUM_LEDS = 149

# Define LED colors
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
OFF = (0, 0, 0)

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SIGNAL_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SIGNAL_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SIGNAL_PIN_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize NeoPixel strip
# Initialize NeoPixel strip
pixels = neopixel.NeoPixel(board.D18, NUM_LEDS)  # Replace D18 with a supported GPIO pin number

# Function to fade yellow lights
def fade_yellow():

    print('hei og hopp')
    for i in range(3):
        for j in range(NUM_LEDS):
            pixels[j] = (int(YELLOW[0] * (1 - i / 3)), int(YELLOW[1] * (1 - i / 3)), 0)
            # if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            #     print('Button pressed, yellowfade exited') -----------UNCOMMENT TO ADD BUTTON BREAK --------------
            #     return False
            time.sleep(0.05)
    return True

            # Function to light up all LEDs in one color
def light_up_all(color):
    pixels.fill(YELLOW)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

async def rainbow_cycle(wait):

    for j in range(255):
        for i in range(NUM_LEDS):
            pixel_index = (i * 256 // NUM_LEDS) + j
            pixels[i] = wheel(pixel_index & 255)
            # if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            #     print('Button pressed, rainbow cycle exited') -------- UNCOMMENT TO ADD BUTTON BREAK
            #     return False
        pixels.show()
        time.sleep(wait)

    return True


# Function to blink green lights
def blink_green():
    for _ in range(5): # Blink 5 times
        pixels.fill(GREEN)
        time.sleep(0.05)
        pixels.fill(OFF)
        time.sleep(0.05)

# Function to blink red lights
def blink_red():
    for _ in range(5): # Blink 5 times
        pixels.fill(RED)
        time.sleep(0.5)
        pixels.fill(OFF)
        time.sleep(0.5)

def fillEveryOtherRedYellow():
    for i in range(NUM_LEDS):
        if i % 2 == 0:
            pixels[i] = RED
        else:
            pixels[i] = YELLOW
    pixels.show()

def shutOff():
    pixels.fill(OFF)
    pixels.show()

# try:
#     print('Loop started')
#     while True:

#         # if GPIO.input(SIGNAL_PIN_1):
#         #     fade_yellow()
#         # elif GPIO.input(SIGNAL_PIN_2):
#         #     blink_green()
#         # elif GPIO.input(SIGNAL_PIN_3):
#         #     blink_red()
#         # else:
#         #     pixels.fill(OFF)
#         # fade_yellow()

#         # fade_yellow()
#         rainbow_cycle(0.1)
#         time.sleep(1)

# except KeyboardInterrupt:
#     GPIO.cleanup()


# while True:
#     # rainbow_cycle(0.0001)  # rainbow cycle with 1ms delay per step
#     # blink_green()
#     # fade_yellow()

def main():
    # rainbow_cycle(0.0001)  # rainbow cycle with 1ms delay per step
    blink_green()
    fade_yellow()


if __name__ == "__main__":
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    main()
    GPIO.cleanup()
    print('GPIO cleaned up')
