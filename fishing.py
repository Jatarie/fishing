import os
from threading import Thread
import re
import time
import win32com.client as comclt
import sys
import random


class GP():

    def __init__(self, gp):
        self.gp = gp
        self.patience_flag = False
        self.cordial_is_up = True
        gp_thread = Thread(target=self.calculate_gp)
        gp_thread.start()

    def calculate_gp(self):
        files = os.listdir(
            "C:\\Users\\Matt\\AppData\\Roaming\\Advanced Combat Tracker\\FFXIVLogs")
        file_ = files[-1]
        start = time.time()
        cordial_timer = 0
        patience_timer = 0

        with open("C:\\Users\\Matt\\AppData\\Roaming\\Advanced Combat Tracker\\FFXIVLogs\\{}".format(file_), "rb") as f:
            f.readlines()

            while True:

                if time.time() - start >= 3:
                    self.gp = min(self.gp+6, 736)
                    start = time.time()

                for line in f:
                    if "You suffer the effect of" in str(line) and time.time() - patience_timer >= 145:
                        print("Patience Used")
                        self.patience_flag = True
                        print("GP Thread Patience flag: {}".format(self.patience_flag))
                        self.gp -= 470
                        patience_timer = time.time()

                    if "You recover 350 GP" in str(line):
                        self.cordial_is_up = False
                        cordial_timer = time.time()
                        self.gp = min(self.gp+350, 736)

                    if self.patience_flag and "You land a" in str(line):
                        self.gp -= 85

                    if time.time() - patience_timer >= 145:
                        print("Patience expired")
                        self.patience_flag = False
                        print("GP Thread Patience flag: {}".format(self.patience_flag))

                if time.time() - cordial_timer >= 216:
                    self.cordial_is_up = True

                time.sleep(.1)


def usb_listener():
    something = bytearray.fromhex("C0 00 4C 4C")
    with open("C:\\Users\\Matt\\Desktop\\Bullshit\\test", "rb") as f:
        f.readlines()
        counter = 0
        start = time.time()
        while True:
            for line in f:
                if something in line:
                    x = re.findall(r'xc0\\x00LL', str(line), re.DOTALL)
                    counter += len(x)
                    start = time.time()
            if time.time() - start > 2 and counter > 0:
                return counter

            time.sleep(0.1)


def log_listener():
    files = os.listdir("C:\\Users\\Matt\\AppData\\Roaming\\Advanced Combat Tracker\\FFXIVLogs")
    file_ = files[-1]
    with open("C:\\Users\\Matt\\AppData\\Roaming\\Advanced Combat Tracker\\FFXIVLogs\\{}".format(file_), "rb") as f:
        f.readlines()
        while True:
            time.sleep(0.1)
            for line in f:
                print(line)
                if "You lose your bait" in str(line):
                    time.sleep(random.uniform(2, 4))
                    return False
                if "Something bites!" in str(line):
                    time.sleep(random.uniform(8, 11))
                    if "You land" not in f.readlines():
                        return True
                    else:
                        return False
                if "You land" in str(line):
                    time.sleep(random.uniform(2, 4))
                    return False


wsh = comclt.Dispatch("Wscript.Shell")


def patience():
    time.sleep(random.uniform(1, 3))
    wsh.SendKeys("{F4}")  # patience

def cordial():
    time.sleep(random.uniform(1, 3))
    wsh.SendKeys("{F10}")  # cordial

def cast():
    time.sleep(random.uniform(1, 3))
    wsh.SendKeys("{F6}")  # cast

def precision():
    wsh.SendKeys("{F7}")  # precision

def normal():
    wsh.SendKeys("{F9}")  # normal

def collectible():
    for _ in range(0, 3):
        wsh.SendKeys("{F8}")  # normal
        time.sleep(random.uniform(1, 2))


def main():
    gp_class = GP(736)

    if usb_listener() == 5:
        normal()

    if log_listener():
        collectible()

    while True:

        print("Main thread: patience flag {}".format(gp_class.patience_flag))
        print(gp_class.gp)


        if gp_class.gp >= 600 and not gp_class.patience_flag:
            patience()
        
        time.sleep(random.uniform(1, 2))

        if gp_class.gp <= 426 and gp_class.cordial_is_up:
            cordial()
        
        cast()

        if usb_listener() == 5:
            if gp_class.patience_flag:
                precision()
            else:
                normal()

        if log_listener():
            collectible()
            
        
main()
