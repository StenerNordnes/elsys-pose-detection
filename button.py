from gpiozero import Button
import time

button = Button(17) #(17) endres når knapp koblet til pin 17 på rasberry pi trykkes
loop_running = False


# Initialize the last press time and the cooldown period
last_press_time = 0
cooldown_period = 5  # Cooldown period in seconds

def toggle_loop():
    global loop_running, last_press_time
    current_time = time.time()
    # Check if the current press is beyond the cooldown period from the last press
    if current_time - last_press_time > cooldown_period:
        loop_running = not loop_running
        last_press_time = current_time  # Update the last press time
        if loop_running:
            print("Loop started. Press the button again to stop.")
        else:
            print("Loop stopped. Ready for another person.")


button.when_pressed = toggle_loop

try:
    while True:
        # Wait for the loop to start
        while not loop_running:
            time.sleep(0.1)
        
        print("Loop started. Press the button to stop.")
        
        # Perform the loop's tasks until the button is pressed again
        while loop_running:
            
            if loop_running:
                img = picam2.capture_array()
                tensor = tf.convert_to_tensor(img)
                newName, conf, frame = predictImage(tensor)

            if conf > 0.999:
                name = newName
                poseConsecutive += 1
            else:
                name = ''
                poseConsecutive = 0

            if poseConsecutive > 10:
                update_score(pasientMap[name], 10)
                poseConsecutive = 0
        else:
            sleep()
            print("Loop is running...")
            time.sleep(1)  # Example task: printing a message every second

        print("Loop stopped. Ready for another person.")

except KeyboardInterrupt:       
    print("Program exited cleanly")





