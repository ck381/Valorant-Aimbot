import keyboard
import time
import mss
import ctypes
import winsound
import PIL.ImageGrab
import PIL.Image
import os
from ahk import AHK
from AutoHotPy import AutoHotPy
from InterceptionWrapper import InterceptionMouseState,InterceptionMouseStroke,InterceptionMouseFlag
from ctypes import *
import ctypes
from ctypes import wintypes

import numpy as np


class bot:

    def __init__(self):
        self.height, self.width = self.get_image_size()
        self.red, self.green, self.blue = (250, 100, 250)  # Colour to look for (Purple)
        self.trigger = '9'
        self.stop = ('8')
        self.x = 0
        self.y = 0
        self.i = 0
        self.j = 0
        self.shot_counter = 1
        self.w = 35
        self.h = 35
        self.width = self.width
        self.height = self.height
        self.total_shots = 0
        self.time = None
        self.triggerBot = False
        self.aim = False



        self.lasti = None
        self.lastj = None

    def get_image_size(self):
        H, W = PIL.ImageGrab.grab().size
        return H,W

    def get_shot(self):
        with mss.mss() as sct:
            a = int(0)
            b = int(0)
            c = int(self.height)
            d = int(self.width)
            bbox=(int(self.height/2-self.h), int(self.width/2-self.w), int(self.height/2+self.h), int(self.width/2+self.w))
            sct_img = sct.grab(bbox)
            result = PIL.Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
            return result


    def click_point(self):
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)


    def moveMouse(self,autohotpy, event):
        import random
        initial_position = (self.x, self.y)
        autohotpy.moveMouseToPosition(initial_position[0], initial_position[1])


    def reset(self,autohotpy,event):
        initial_position = (960,540)
        autohotpy.moveMouseToPosition(initial_position[0], initial_position[1])



    def search(self,auto):


        import random

        import ctypes
        from ctypes import wintypes

        BlockInput = ctypes.windll.user32.BlockInput
        BlockInput.argtypes = [wintypes.BOOL]
        BlockInput.restype = wintypes.BOOL

        blocked = BlockInput(True)

        array = self.get_shot()
        a = False
        array = np.array(array)
        counter = 0


        x_values = []
        y_values = []



        for i in range(0,self.w * 2):
            for j in range(0, self.h * 2):
                r,g,b, = array[i][j]
                if self.estimate(r,g,b):
                    if self.estimate(r, g, b) and counter < 1:


                        if self.total_shots == 0:
                            self.time = time.time()
                        if self.total_shots >= 4:
                            now = time.time()
                            if now - self.time < 0.08:
                                print(now - self.time)
                                time.sleep(0.01)
                            self.total_shots = 0



                        vecX = (960 - self.w) + j
                        vecY = 540

                        vector_1 = [960, 540]
                        vector_2 = [vecX, vecY]
                        unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
                        unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
                        dot_product = np.dot(unit_vector_1, unit_vector_2)
                        angle = np.arccos(dot_product)
                        degree = self.width / 103
                        x = angle * degree

                        if j > self.w:
                            self.x = x
                        else:
                            self.x = x * -1

                        vecX = 960
                        vecY = (540 - self.h) + i

                        vector_1 = [960, 540]
                        vector_2 = [vecX, vecY]
                        unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
                        unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
                        dot_product = np.dot(unit_vector_1, unit_vector_2)
                        angle = np.arccos(dot_product)
                        degree = self.height / 71
                        x = angle * degree


                        if i > self.h:
                            self.y = x
                        else:
                            self.y = x * -1


                        self.i = i
                        self.j = j
                        counter = 1

                        auto.registerForMouseMovement(bot.moveMouse)
                        auto.start()

                        print(self.x,self.y)

                        if self.x < 0.1 and self.x + -0.1 and self.y < 0.1 and self.y > -0.1:
                            self.click_point()

                        #blocked = BlockInput(False)







    def estimate(self, r, g, b):
        return self.red - 55 < r < self.red + 55 and self.green - 55 < g < self.green + 55 and self.blue -  55 < b < self.blue + 55





def exitAutoHotKey(autohotpy,event):
    """
    exit the program when you press ESC
    """
    autohotpy.stop()

def startStopMacro(autohotpy,event):
    global initial_position
    if not autohotpy.isRecording():
        initial_position  = autohotpy.getMousePosition()
    autohotpy.macroStartStop()




def moveHandler(autohotpy,event):
    """
    This function inverts mouse axis!
    """
    if not(event.flags & InterceptionMouseFlag.INTERCEPTION_MOUSE_MOVE_ABSOLUTE):
        event.x *= -1
        event.y *= -1
    autohotpy.sendToDefaultMouse(event)


if __name__ == "__main__":
    bot = bot()
    auto = AutoHotPy()
    auto.registerExit(auto.ESC,exitAutoHotKey)  # Registering an end key is mandatory to be able tos top the program gracefully
    running = False
    while True:



        if keyboard.is_pressed(bot.trigger):
            running = True
        if keyboard.is_pressed(bot.stop):
            running = False
        if running:
            bot.search(auto)




