from bomb_keypad import wait_for_key
            
from bomb_sound import beeping
from machine import Pin
import time

pin_28 = Pin(28, Pin.OUT)
pin_28.value(0)  # Explicitly set the pin low

correctpassword = ['7', '3', '5', '5', '6', '0', '8']


def has_bomb_been_planted(correctpassword):
    password = key()
    while True:
        if password == correctpassword:
            greeting("Bomb has been planted.")

def main(correctpassword):
    password = []
    while True:
        keyPress = wait_for_key()
        password.append(keyPress)
        print(password)
        if password == correctpassword:
            greeting("7 3 5 5 6 0 8")
            time.sleep(1)
            greeting("Correct")
            time.sleep(0.7)
            greeting("The bomb is now planted.")
            beeping()
            greeting("You are dead!")
            exit
        if len(password) == 7:
            password = []
        greeting(password)
main(correctpassword)
#has_bomb_been_planted()