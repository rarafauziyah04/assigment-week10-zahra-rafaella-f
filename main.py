import time
import requests
import math
import random
from tkinter import Variable
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import time


TOKEN = "BBFF-kWG4xvGbYeO2Yjy80WpBbnbg8XAUCB"  # Put your TOKEN here
DEVICE_LABEL = "demo"  # Put your device label here 
VARIABLE_LABEL_1 = "LDR"  # Put your first variable label here
VARIABLE_LABEL_2 = "SUHU"
VARIABLE_LABEL_3 = "KELEMBABAN"

    



def build_payload(varia_1, varia_2, varia_3):

    GPIO.setmode(GPIO.BOARD)
    varia_1 = 8

    hitung = 0

    GPIO.setup(varia_1, GPIO.OUT)
    GPIO.output(varia_1, GPIO.LOW)
    time.sleep(5)
    GPIO.setup(varia_1, GPIO.IN)
  
    while (GPIO.input(varia_1) == GPIO.LOW):

        hitung += 1
    
    sensor = Adafruit_DHT.DHT11
    pin = 4
    kelembaban, suhu = Adafruit_DHT.read(sensor, pin)



    value_1 = hitung
    value_2 = suhu
    value_3 = kelembaban
    

   

    payload = {varia_1: value_1,
               varia_2: value_2,
               varia_3: value_3}

    return payload

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


    


if _name_ == '_main_':
    while (True):
        main()
        time.sleep(1)