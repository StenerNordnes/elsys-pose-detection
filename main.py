from colors import fade_yellow, rainbow_cycle, blink_green, blink_red, shutOff, fillEveryOtherRedYellow
import RPi.GPIO as GPIO  # Importerer GPIO-biblioteket for å kontrollere Raspberry Pi GPIO-pinner
import time  
from camtest import cameraMain 
import asyncio  

GPIO.setwarnings(False)  # Ignorerer advarsler for nå

push_count = 0  
is_running = False 


def button_callback(channel):  # Tilbakekallsfunksjon som vil bli kalt når knappen trykkes
    global push_count  
    global is_running  
    if is_running:  # Hvis knappen allerede kjører, skriv ut en melding og returner
        print('Button is already running')
        return
    
    is_running = True  

    print("Button was pushed!")

    fillEveryOtherRedYellow()  # Initialiserer lyset til poserings mode
    wasSucessful = cameraMain()  # CameraMain håndterer poseringsgjenkjenning og returnerer True hvis posen ble gjenkjent, ellers False

    if wasSucessful:  # Blinker grønt ved vellykket posering
        blink_green()
    else:  # Blinker rødt ved mislykket posering
        blink_red()

    
    time.sleep(1)  
    push_count += 1 
    is_running = False 

    asyncio.create_task(rainbow_cycle(0.1))  # Oppretter asynkron idle state når den venter på en ny deteksjon
    print('Button callback finished')
    time.sleep(1)  

async def main():  
    try:
        GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Setter opp pin 15 som en inngangspinne og setter initialverdien til å være trukket lav (av)
        GPIO.add_event_detect(15, GPIO.RISING, callback=button_callback, bouncetime=1000)  # En hendelsesdeteksjon på stigende flanke for pin 15 med en rebound-tid på 1000 ms som starter en deteksjon
        task = asyncio.create_task(rainbow_cycle(0.1))  
        input("Press Enter to stop...")  # En input som holder programmet slik at knappen kan brukes

    except Exception as e:  # Hvis en unntak oppstår, skriv ut feilmeldingen
        print(f"An error occurred: {str(e)}")

    finally:
        GPIO.cleanup()  


asyncio.run(main()) 