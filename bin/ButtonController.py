import os
import threading
import time
import subprocess
from os.path import isfile, join
from os import listdir
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
        availableScriptNames = self.getScriptNames()
        if self.ackStatus:
            # Write here code that will be executed When the Button is pressed long & the current AckStatus is True
            # and we need to test one more thing
            scriptName = settings['dropdown3']
            if scriptName is not "---" and scriptName in availableScriptNames:
                try:
                    txt = path + scriptName
                    subprocess.call(txt)
                except:
                    print 'cannot open', scriptName

        else:
            # Write here code that will be executed When the Button is pressed long & the current AckStatus is False 
            scriptName = settings['dropdown4']
            if scriptName is not "---" and scriptName in availableScriptNames:
                try:
                    txt = path + scriptName
                    subprocess.call(txt)
                except:
                    print 'cannot open', scriptName

    def shortPress(self):
        path = "/var/lib/crystal-signal/scripts/"
        print "short press!"
        settings = self.getButtonSettings()
        availableScriptNames = self.getScriptNames()
        if self.ackStatus:
            # Write here code that will be executed When the Button is pressed short & the current AckStatus is True
            scriptName = settings['dropdown1']
            if scriptName is not "---" and scriptName in availableScriptNames:
                try:
                    txt = path + scriptName
                    subprocess.call(txt)
                except:
                    print 'cannot open', scriptName

        else:
            # Write here code that will be executed When the Button is pressed short & the current AckStatus is False 
            scriptName = settings['dropdown2']
            if scriptName is not "---" and scriptName in availableScriptNames:
                try:
                    txt = path + scriptName
                    subprocess.call(txt)
                except:
                    print 'cannot open', scriptName
    def getButtonSettings(self):
        path = "/var/lib/crystal-signal/ScriptSettings.json"
        if not isfile(path):
            buttonSettingsInit = {'dropdown1': "---",
                                  'dropdown2': "---",
                                  'dropdown3': "---",
                                  'dropdown4': "---",
                                  'dropdown5': "---"}
            with open(path, 'w+') as outfile:
                json.dump(buttonSettingsInit, outfile)
        with open(path) as data:
            return json.load(data)
    def getScriptNames(self):
        path = "/var/lib/crystal-signal/scripts"
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        return onlyfiles


# - - - - - - - - - - - - - - - - 
# - - - - - - MEMO  - - - - - - -
# - - - - - - - - - - - - - - - -

