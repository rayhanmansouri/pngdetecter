from flask import Flask, send_from_directory
import threading
import pyautogui
import cv2
import numpy as np
import time

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/manifest.webmanifest')
def manifest():
    return send_from_directory('.', 'manifest.webmanifest')

@app.route('/service-worker.js')
def sw():
    return send_from_directory('.', 'service-worker.js')

@app.route('/start')
def start_bot():
    threading.Thread(target=run_bot).start()
    return "Bot gestartet"

def run_bot():
    png_path = "bild.png"
    move_distance_cm = 13
    pixel_per_cm = 37.8

    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(png_path, cv2.IMREAD_COLOR)
    w, h = template.shape[1], template.shape[0]

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.8:
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        offset = int(move_distance_cm * pixel_per_cm)
        target_x = center_x + offset
        target_y = center_y
        pyautogui.moveTo(target_x, target_y, duration=0.5)

        before = pyautogui.screenshot(region=(target_x, target_y, 1, 1))
        time.sleep(0.5)
        while True:
            after = pyautogui.screenshot(region=(target_x, target_y, 1, 1))
            if after != before:
                pyautogui.scroll(-300)
                break
            time.sleep(0.5)

if __name__ == '__main__':
    app.run(port=5000)
