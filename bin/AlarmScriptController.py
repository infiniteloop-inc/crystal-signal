import os
import threading
import time
import subprocess
from os.path import isfile, join
from os import listdir
import json

# - - - - - - - - - - - - - - - - - -
# -  ALARM SCRIPT CONTROLLER CLASS  -  
# - - - - - - - - - - - - - - - - - - 
class AlarmScriptController:
    def __init__(self):
        pass;
    def executeAlarmScript(self):
        path = "/var/lib/crystal-signal/scripts/"
        settings = self.getScriptSettings()
        availableScriptNames = self.getScriptNames()
        scriptName = settings['dropdown5']
        if scriptName is not "Do Nothing" and scriptName in availableScriptNames:
            try:
                txt = path + scriptName
                subprocess.call(txt)
            except:
                print 'cannot open', scriptName
    def getScriptSettings(self):
        path = "/var/lib/crystal-signal/ScriptSettings.json"
        if not isfile(path):
            buttonSettingsInit = {'dropdown1': "Do Nothing",
                                  'dropdown2': "Do Nothing",
                                  'dropdown3': "Do Nothing",
                                  'dropdown4': "Do Nothing",
                                  'dropdown5': "Do Nothing"}
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

