import os
import time
from threading import Thread


print(time.time())
class GP():

    def __init__(self, gp):
        self.gp = gp
        gp_thread = Thread(target=self.calculate_gp)
        gp_thread.start()

    def calculate_gp(self):
        files = os.listdir("C:\\Users\\Matt\\AppData\\Roaming\\Advanced Combat Tracker\\FFXIVLogs")
        file_ = files[-1]
        start = time.time()
        patience_flag = False
        with open("C:\\Users\\Matt\\AppData\\Roaming\\Advanced Combat Tracker\\FFXIVLogs\\{}".format(file_), "rb") as f:
            f.readlines()
            while True:
                if time.time() - start >= 3:
                    self.gp += 6
                    if self.gp > 736:
                        self.gp = 736
                    start = time.time()
                    for line in f:
                        if "You suffer the effect of" in str(line):
                            patience_flag = True
                            print("yes")
                            self.gp -= 470
                        if "You recover 300 GP" in str(line):
                            self.gp += 300
                        if patience_flag and "You land a" in str(line):
                            self.gp -= 85

                time.sleep(1)