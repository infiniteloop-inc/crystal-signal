import os
import socket
import threading
import SocketServer
import time
from random import randint
import subprocess
from os import listdir
from os.path import isfile, join
import json

# - - - - - - - - - - - - - - - - 
# - - BUTTON CONTROLLER CLASS - -
# - - - - - - - - - - - - - - - -
class ButtonController:
    def __init__(self):
        self.buttonPressedFlag = False 
        self.helperFlag1 = False 
        self.buttonReleasedCounter = 0
        self.longPressTime = 1000;      # All time related properties in Millisecs 
        self.pressStartTime = 0;
        self.pressEndTime = 0;
        self.pressDuration = 0
        self.ackStatus = False;
    def update(self, buttonStatus, ackStatus):
        self.ackStatus = ackStatus
        if buttonStatus and not self.helperFlag1:
            # Trigger on positive flank of Button Input Signal
            self.buttonPressedFlag = True;
            self.helperFlag1 = True
            self.pressStartTime = self.getTimeStamp()
            # helperFlag1 needs to be resetted after the Buttonpress was registered correctly
        elif not buttonStatus and self.buttonPressedFlag:
            # We get in here when the button was pressed but isn't pressed anymore
            self.buttonReleasedCounter += 1;
            if self.buttonReleasedCounter >= 2:
                self.buttonPressedFlag = False
                self.helperFlag1 = False
                self.buttonReleasedCounter = 0
                self.pressEndTime = self.getTimeStamp()
                self.pressDuration = self.pressEndTime - self.pressStartTime
                if self.pressDuration >= self.longPressTime:
                    # Long Press!
                    self.longPress()
                else:
                    # Short Press!
                    self.shortPress()
        elif buttonStatus and self.buttonPressedFlag:
            # Reset the buttonReleasedCounter if the buttonStatus gets high again very fast
            self.buttonReleasedCounter = 0;
    def getTimeStamp(self):
        # returns the current TimeStamp in millisecs
        return int(time.time()*1000)
    def longPress(self):
        path = "/var/lib/crystal-signal/scripts/"
        settings = self.getButtonSettings()
        if self.ackStatus:
            # Write here code that will be executed When the Button is pressed long & the current AckStatus is True
            # and we need to test one more thing
            scriptName = settings['dropdown3']
            #self.sendingDataToLEDController("color=171,148,100&mode=2&repeat=0&period=2000&json=0")
            if scriptName is not "Do Nothing":
                try:
                    txt = path + scriptName
                    subprocess.call(txt)
                except:
                    print 'cannot open', scriptName

        else:
            # Write here code that will be executed When the Button is pressed long & the current AckStatus is False 
            scriptName = settings['dropdown4']
            #self.sendingDataToLEDController("ack=1")
            if scriptName is not "Do Nothing":
                try:
                    txt = path + scriptName
                    subprocess.call(txt)
                except:
                    print 'cannot open', scriptName

    def shortPress(self):
        path = "/var/lib/crystal-signal/scripts/"
        print "short press!"
        settings = self.getButtonSettings()
        if self.ackStatus:
            # Write here code that will be executed When the Button is pressed short & the current AckStatus is True
            scriptName = settings['dropdown1']
            #self.sendRandomColorInstruction()
            if scriptName is not "Do Nothing":
                try:
                    txt = path + scriptName
                    subprocess.call(txt)
                except:
                    print 'cannot open', scriptName

        else:
            # Write here code that will be executed When the Button is pressed short & the current AckStatus is False 
            scriptName = settings['dropdown2']
            #self.sendingDataToLEDController("ack=1")
            if scriptName is not "Do Nothing":
                try:
                    txt = path + scriptName
                    subprocess.call(txt)
                except:
                    print 'cannot open', scriptName

    def sendRandomColorInstruction(self):
        red = str(randint(0,255))
        green = str(randint(0,255))
        blue = str(randint(0,255))
        self.sendingDataToLEDController("color=" + red + "," + green + "," + blue + "&mode=1&repeat=0&period=700&json=0")
    def sendingDataToLEDController(self, query_string):
        client('localhost', 7777, query_string + "&remote_addr=" + "ButtonController")
    def getButtonSettings(self):
        path = "/var/lib/crystal-signal/ButtonSettings.json"
        if not isfile(path):
            buttonSettingsInit = {'dropdown1': "Do Nothing",
                                  'dropdown2': "Do Nothing",
                                  'dropdown3': "Do Nothing",
                                  'dropdown4': "Do Nothing"}
            with open(path, 'w+') as outfile:
                    json.dump(buttonSettingsInit, outfile)
        with open(path) as data:
            return json.load(data)


# - - - - - - - - - - - - - - - - 
# - - - SOCKET CLIENT CLASS - - -
# - - - - - - - - - - - - - - - -
def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        # wait for the python script to produce and send the data
        time.sleep(0.3)
        response = sock.recv(1048576)
        # we do not neet to print the responce
        # print "Content-type: text/html \n\n"
        # print response
    finally:
        sock.close()


# - - - - - - - - - - - - - - - - 
# - - - - - - MEMO  - - - - - - -
# - - - - - - - - - - - - - - - -

