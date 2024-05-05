import cv2
import numpy as np
import threading
import time
import mss

# Function to capture screen
def capture_screen():
    global is_running
    while is_running:
        # Capture screen
        img = np.array(sct.grab(monitor))
        # Convert BGR to RGB
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        # Display the frame
        cv2.imshow('Screen', frame)
        # Break the loop on 'q' key press
        if cv2.waitKey(1) == ord('q'):
            is_running = False
            break

# Function to handle user interaction
def user_interaction():
    global is_running
    while is_running:
        # Example of interaction, here you can perform your tasks
        print("Doing some tasks while capturing screen...")
        time.sleep(1)  # Sleep for 1 second

# Initialize mss
sct = mss.mss()

# Get monitor resolution
mon = sct.monitors[1]  # Change index if necessary
monitor = {
    "top": mon["top"],
    "left": mon["left"],
    "width": mon["width"],
    "height": mon["height"],
}

# Global variable to control the loop
is_running = True

# Create and start threads
capture_thread = threading.Thread(target=capture_screen)
interaction_thread = threading.Thread(target=user_interaction)

capture_thread.start()
interaction_thread.start()

# Wait for threads to finish
capture_thread.join()
interaction_thread.join()

# Release resources
cv2.destroyAllWindows()