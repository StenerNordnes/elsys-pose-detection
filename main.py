from colors import fade_yellow, rainbow_cycle, blink_green, blink_red, shutOff, fillEveryOtherRedYellow
from camtest import cameraMain
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False) # Ignore warning for now

push_count = 0
is_running = False



def button_callback(channel):
    global push_count
    global is_running
    if is_running:
        print('Button is already running')
        return
    
    is_running = True

    looper = push_count % 1
    print("Button was pushed!", looper)

    if looper == 0:
        fillEveryOtherRedYellow()
        wasSucessful = cameraMain()
        if wasSucessful:
            blink_green()
        else:
            blink_red()
    
    time.sleep(1)
    push_count += 1
    is_running = False
    isIdleRunning = True

    while isIdleRunning:
        isIdleRunning = rainbow_cycle(0.1)

        if not isIdleRunning:
            shutOff()
            break
    
    print('Button callback finished')

    time.sleep(1)



try:
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 23 to be an input pin and set initial value to be pulled low (off)
    # # Setup event on pin 23 rising edge with debounce time
    # GPIO.add_event_detect(15, GPIO.RISING, callback=button_callback, bouncetime=1000)
    # input("Press Enter to stop...")

    GPIO.add_event_detect(15, GPIO.RISING, callback=lambda x: print('pressed down'), bouncetime=1000)
    while True:
        time.sleep(0.1)
        print('waiting for button press')


except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    GPIO.cleanup()