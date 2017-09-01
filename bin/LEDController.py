#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import math
import time
import json
import pigpio
import urllib
import random
import datetime
import threading
import SocketServer
from os import listdir
from os.path import isfile, join, splitext
from ButtonController import ButtonController
from AlarmScriptController import AlarmScriptController
from SpeakMessageController import SpeakMessageController 

# - - - - - - - - - - - - - - - -
# - - - - SOCKET CLASSES  - - - -
# - - - - - - - - - - - - - - - -
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        ledCtrl.updateStatus(data)
        response = ledCtrl.getStatus()
        self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

# - - - - - - - - - - - - - - - -
# - - LED CONTROLLER CLASS  - - -
# - - - - - - - - - - - - - - - -
class LEDController:
    def __init__(self):
        self.pi1 = pigpio.pi('localhost', 8888)
        self.buttonController = ButtonController()
        self.alarmScriptController = AlarmScriptController()
        self.speakMsgController = SpeakMessageController("/var/lib/crystal-signal/sounds/speakMsg.wav")
        self.pinList = [14, 15, 18]
        self.pi1.set_mode(4, pigpio.INPUT)
        self.pi1.set_pull_up_down(4, pigpio.PUD_OFF)
        self.queryString = ""
        self.statusDict = {
                       'color': [0,0,0],    # 0 ~ 255 rgb
                        'mode': 0,          # 0 -> constant on, 1 -> blinking, 2: asynchron blinking
                      'period': 1000,       # in milliseconds
                      'repeat': 0,          # if x > 0 -> stop after blinking x times
                         'ack': 1,          # was the current alarm acknowledged? 0 -> NO, 1 -> YES
                        'json': 0,          # 0 -> status response in HTML, 1 -> status response in Json
                        'info': "",         # info
                        'speak': "",        # speak Message (japanese only) 
                        'remote_addr': 0,   # Where was the request sent from?
                        'remote_host': 0    # What is the name of the request sender?
                        }   
        self.listOfKeys = ['color', 'period', 'repeat', 'mode', 'ack', 'json', 'info', 'speak']
        self.explanationDict = {
                        'color': "rgb values from 0 ~ 255",
                        'period': "length of blinking period (in millisecs)",
                        'repeat': "if x > 0 -> stop after blinking x times",
                          'mode': "0-> ON, 1-> blinking, 2-> blinking asynchronously",
                           'ack': "parameter to acknowledge an alert / blinking pattern",
                          'json': "0 -> status response in HTML, 1 -> status response in Json",
                          'info': "information about the alert",
                          'speak': "let the Raspberry Pi speak on alert (japanese only)"
                          }
        self.logList = []
        self.brightness = self.getBrightnessSetting()
        self.setupPWM()
        self.resetUpdateParaMode1()
        self.resetUpdateParaMode2()
        self.newStatusFlag = True;
        self.argList = []

    def updateStatus(self, query_string):
        self.newStatusFlag = True;
        self.noScript = False;
        self.getLogData = False;
        self.getDropDownData = False;
        self.settingUpButtons = False;
        self.settingUpSettings = False;
        colorWasSet = False
        self.queryString = query_string
        self.argList=query_string.split('&')
        for arg in self.argList:
            if arg is not "":
                key, value=arg.split('=')
                key = key.lower()
                if key == 'ack':
                    if int(value) != 0:
                        self.statusDict['ack'] = 1
                        # an ack was sent. This means we have to set all the acks in the logList!
                        self.setAcksInLogList()
                    else:
                        self.statusDict['ack'] = 0
                elif key == 'ackone':
                    if int(value) != 0:
                        self.statusDict['ack'] = 1
                        self.acknowledgeNewestAlarm()
                elif key == 'deletelog':
                    if int(value) != 0:
                        self.deleteLog()
                elif key == 'getlogdata':
                    if int(value) != 0:
                        self.getLogData = True
                elif key == 'getdropdowndata':
                    if int(value) != 0:
                        self.getDropDownData = True
                elif key == 'settingupbuttons':
                    if int(value) != 0:
                        self.settingUpButtons = True
                elif key == 'settingupsettings':
                    if int(value) != 0:
                        self.settingUpSettings = True
                elif key == 'noscript':
                    if int(value) != 0:
                        self.noScript = True
                elif key == 'json':
                    if int(value) != 0:
                        self.statusDict['json'] = 1
                    else:
                        self.statusDict['json'] = 0
                elif key == 'color':
                    colorWasSet = True
        if  colorWasSet:   # Only load the other parameters if at least 1 color parameter was sent
            self.resetStatusDict()
            for arg in self.argList:
                key, value=arg.split('=')
                key = key.lower()
                if key in self.statusDict:
                    if key == 'color':
                        valueArr = urllib.unquote(value).split(',')
                        for index, element in enumerate(valueArr):
                            self.statusDict['color'][index] = int(element)
                    else:
                        try:                # Test weather or not the thing can be converted to an int
                            self.statusDict[key] = int(value)
                        except ValueError:
                            self.statusDict[key] = value
            self.checkBoundries()

            self.speakIfNecessary()

            clonedDict = dict(self.statusDict)
            clonedDict['date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.logList.insert(0, clonedDict)

            # delete last items from list if list contains more then 500 entries
            if len(self.logList) > 500:
                self.logList.pop()

            self.resetUpdateParaMode1()
            self.resetUpdateParaMode2()
            if not self.noScript:
                self.alarmScriptController.executeAlarmScript()

    def speakIfNecessary(self):
        speakMsg = urllib.unquote(str(self.statusDict['speak']))
        if speakMsg is not "":
            self.speakMsgController.createAndPlayAudio(speakMsg)

    def constantOn(self):
        if self.newStatusFlag:
            for index, pin in enumerate(self.pinList):
                self.pi1.set_PWM_dutycycle(pin, self.statusDict['color'][index])
            self.newStatusFlag = False
        # sleep for 100ms
        time.sleep(0.1)

    def blinking(self):
        if self.stepCounter < self.numOfSteps:
            self.stepCounter += 1
        else:
            self.halfPeriodCounter += 1
            self.periodCounter = self.halfPeriodCounter / 2
            if self.statusDict['repeat'] > 0 and self.periodCounter >= self.statusDict['repeat']:
                self.repeatEnded = True
            self.stepCounter = 0
            self.risingEdge = not self.risingEdge
        for index, pin in enumerate(self.pinList):
            if self.risingEdge:
                self.pi1.set_PWM_dutycycle(pin, int(self.statusDict['color'][index] *
                    (math.cos(self.stepCounter / float(self.numOfSteps) * math.pi - math.pi) / 2.0 + 0.5)))
            else:
                self.pi1.set_PWM_dutycycle(pin, int(self.statusDict['color'][index] * 
                    ( 1 - (math.cos(self.stepCounter / float(self.numOfSteps) * math.pi - math.pi) / 2.0 + 0.5))))
        time.sleep(self.stepDuration / 1000.0)

    def asynchBlinking(self):
        for index, pin in enumerate(self.pinList):
            if self.getTimeInMilliSec() > self.oldTimeM2[index] + self.stepDurationM2[index]:
                self.oldTimeM2[index] = self.getTimeInMilliSec()
                if self.stepCounterM2[index] < self.numOfSteps:
                    self.stepCounterM2[index] += 1
                else:
                    self.stepCounterM2[index] = 0
                    self.risingEdgeM2[index] = not self.risingEdgeM2[index]
                if self.risingEdgeM2[index]:
                    self.pi1.set_PWM_dutycycle(pin, int(self.statusDict['color'][index] *
                        (math.cos(self.stepCounterM2[index] / float(self.numOfSteps) * math.pi - math.pi)/2.0 + 0.5)))
                else:
                    self.pi1.set_PWM_dutycycle(pin, int(self.statusDict['color'][index] *
                        ( 1 - (math.cos(self.stepCounterM2[index] / float(self.numOfSteps) * math.pi - math.pi)/2.0 + 0.5))))
        time.sleep(0.5 * self.stepDuration / 1000.0)

    def update(self):
        self.buttonController.update(self.pi1.read(4), self.statusDict['ack'])
        if self.statusDict['ack'] != 0 or self.repeatEnded:
            if self.newStatusFlag:
                self.resetLEDs()
                self.newStatusFlag = False
            time.sleep(0.1)
        else:
            if self.statusDict['mode'] == 0:
                self.constantOn()
            elif self.statusDict['mode'] == 1:
                self.blinking()
            elif self.statusDict['mode'] == 2:
                self.asynchBlinking()
            else:
                # sleep for 100ms if there's nothing to do
                time.sleep(0.1)

    def getTimeInMilliSec(self):
        return int(time.time()*1000)

    def resetStatusDict(self):
        self.statusDict['color'] = [0,0,0]
        self.statusDict['period'] = 1000
        self.statusDict['ack'] = 0
        self.statusDict['repeat'] = 0 # don't repeat unless explicitly told to do so
        self.statusDict['json'] = 0
        self.statusDict['info'] = ""
        self.statusDict['speak'] = ""

    def resetLEDs(self):
        for pin in self.pinList:
            self.pi1.set_PWM_dutycycle(pin, 0)

    def resetUpdateParaMode1(self):
        self.halfPeriodCounter = 0
        self.periodCounter = 0
        self.repeatEnded = False
        self.numOfSteps = round(self.statusDict['period'] / 10.0) + 1
        self.stepDuration = self.statusDict['period'] / (self.numOfSteps * 2)
        self.stepCounter = 0
        self.risingEdge = True

    def getStatus(self):
        if self.getLogData:
            # Here we need to return a nicely formatted table!
            # something like this:
            return self.getTableHTML()
        elif self.getDropDownData:
            # Here we need to return some Bootstrap Dropdown menus!
            return self.getDropDownHTML()
        elif self.settingUpButtons:
            # This is the area where we manage the ScriptSettings.json file.
            # we do not even need to return anything.
            self.setScriptSettings()
            return ""
        elif self.settingUpSettings:
            # This is the erea where we manage the Settings.json file.
            # we do not even need to return anything.
            self.setSettings()
            self.brightness = self.getBrightnessSetting()
            self.setupPWMRange()
            return ""
        else:
            if self.statusDict['json'] == 0:
                argList = ""
                argExplanation = ""
                clonedDict = dict(self.statusDict)
                for key in self.listOfKeys:
                    argList += key + ": " + str(self.statusDict[key]) + "<br>\r\n"
                for key in self.listOfKeys:
                    argExplanation += "<b>" + key + ":</b> " + self.explanationDict[key] + "<br>\r\n"
                response = "<h2>Argument list</h2>\r\n" + argList + \
                "\r\n<h2>Argument Explanation</h2>\r\n" + argExplanation
                return response
            else:
                return json.dumps(self.statusDict)

    def deleteLog(self):
        self.logList = []

    def getTableHTML(self):
        html = ""
        html +=''' <table class="table">
                    <thead>
                      <tr>
                        <th>Date</th>
                        <th>IP Address</th>
                        <th>Parameter</th>
                        <th>Info</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>'''
        for ent in self.logList:
            info = urllib.unquote(str(ent['info']))
            argList = ""
            for key in self.listOfKeys:
                argList += key + ": " + urllib.unquote(str(ent[key])) + "<br>\r\n"
            html += '<tr class="{0}">'.format("danger" if (ent['ack'] == 0) else "success")
            html += "<td>" + ent['date'] + "</td>"
            html += "<td>" + ent['remote_addr'] + "</td>"
            html += '''<td><a href="javascript://" title="Parameter" data-toggle="popover" data-placement="right"
                         data-html="true" data-content="''' + argList + '">color=' + \
                         str(ent['color'][0]) + "," + str(ent['color'][1]) + "," + str(ent['color'][2]) + '...</a></td>'
            if info == "":
                html += "<td></td>"
            elif len(info) <= 9:
                # in case the info text is quite small we don't need to add to the end of the string "..."
                html += '''<td><a href="javascript://" title="Info" data-toggle="popover" data-placement="right"
                            data-html="true" data-content="''' + info  + '">' + info  + '</a></td>'
            else:
                cutOffCor = self.getStringCutOffCorVal(info)
                html += '''<td><a href="javascript://" title="Info" data-toggle="popover" data-placement="right"
                            data-html="true" data-content="''' + info  + '">' + info[:9+cutOffCor]  + '...</a></td>'
            if ent['ack'] == 0:
                html += "<td>pending</td></tr>"
            else:
                html += "<td>acknowledged</td></tr>"
        # and in the end, we need to get the footer thing.
        html += '''</tbody>
                  </table>
                  <script>
                    $('[data-toggle="popover"]').popover();
                  </script>'''
        return html

    def getDropDownHTML(self):
        keyList = ['dropdown1', 'dropdown2', 'dropdown3', 'dropdown4', 'dropdown5']
        htmlList = []
        scriptFileNames = self.getScriptNames()
        scriptFileNames.append("---")
        settings = self.getScriptSettings()
        # Here we check whether or not all the loaded settings entries
        # are either the name of an existing script or "---"
        # make the entry "---" if this is not the case
        rewriteSettingsFlag = False
        for ent in keyList:
            if not settings[ent] in scriptFileNames:
                settings[ent] = "---"
                rewriteSettingsFlag = True
        if rewriteSettingsFlag:
            with open('/var/lib/crystal-signal/ScriptSettings.json', 'w+') as outfile:
                json.dump(settings, outfile)
        for ent in keyList:    # There are 5 DropDown Buttons.
            html =  ''' <div class="dropdown">
                            <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" name="dropDown1">'''
            html +=         urllib.unquote(settings[ent]) + '''<span class="caret"></span></button>
                            <ul class="dropdown-menu">'''
            for entry in scriptFileNames:
                html +=     '<li><a href="#">' + entry + '</a></li>'

            html += '''     </ul>
                        </div>'''
            htmlList.append(html)
        # dropdown nr. 6 is different from the other 5 dropdowns.
        # It's not about scripts but about languages, that's why it's html
        # are set seperatly
        currentLanguage = self.getLanguageSetting()
        availableLanguages = self.getAvailableLanguages()
        html =  ''' <div class="dropdown">
                        <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown" name="dropDown1">'''
        html +=         urllib.unquote(currentLanguage) + '''<span class="caret"></span></button>
                        <ul class="dropdown-menu">'''
        for entry in availableLanguages:
            html +=     '<li><a href="#">' + entry + '</a></li>'

        html += '''     </ul>
                    </div>'''
        htmlList.append(html)
        # also add the slider HTML
        html = '''<input id="sldrBrightness" data-slider-id='SliderBrightness' type="text" data-slider-min="40" data-slider-max="100" data-slider-step="1" data-slider-value="'''
        html += str(round(self.getBrightnessSetting()*60/255.0 + 40)) + '"/>'
        htmlList.append(html)
        return json.dumps(htmlList)

    def setAcksInLogList(self):
        for ent in self.logList:
            if 'ack' in ent:
                ent['ack'] = 1

    def acknowledgeNewestAlarm(self):
        flag = False
        for ent in self.logList:
            if not flag and ent['ack'] == 0:
                ent['ack'] = 1
                flag = True

            if flag and ent['ack'] == 0:
                self.newStatusFlag = True;

                # here we loop through all the subentries of the alarm we need to load back into the
                # self.statusDict
                for key in self.listOfKeys:
                    self.statusDict[key] = ent[key]

                self.speakIfNecessary()

                # after we loaded the values back into the status dict
                # we reset the update parameters
                self.resetUpdateParaMode1()
                self.resetUpdateParaMode2()
                break

    def resetUpdateParaMode2(self):
        durTmp = self.statusDict['period'] / self.numOfSteps
        self.stepDurationM2 = [int((random.random()-0.5)*durTmp + durTmp),
                               int((random.random()-0.5)*durTmp + durTmp),
                               int((random.random()-0.5)*durTmp + durTmp)]
        self.stepCounterM2 = [0,0,0]
        self.oldTimeM2 = [0,0,0]
        self.risingEdgeM2 = [True, True, True]

    def setupPWM(self):
        for pin in self.pinList:
            self.pi1.set_PWM_frequency(pin,600)
            self.pi1.set_PWM_range(pin, 255 + int(745*(255-self.brightness)/255.0))  #1000
            self.pi1.set_PWM_dutycycle(pin, 0)

    def setupPWMRange(self):
        for pin in self.pinList:
            self.pi1.set_PWM_range(pin, 255 + int(745*(255-self.brightness)/255.0))  #1000

    def checkBoundries(self):
        for index, _ in enumerate(self.pinList):
            if self.statusDict['color'][index] > 255:
                self.statusDict['color'][index] = 255
            elif self.statusDict['color'][index] < 0:
                self.statusDict['color'][index] = 0

    def getStringCutOffCorVal(self, string):
        notASCIICounter = 0
        cutOffCor = 0
        for i in range(0,9):
            try:
                string[i].decode('ascii')
            except:
                notASCIICounter += 1
        tmp = notASCIICounter%3
        cutOffCor = 3-tmp if tmp>0 else tmp
        return cutOffCor

    def getScriptNames(self):
        path = "/var/lib/crystal-signal/scripts"
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        return onlyfiles

    def setScriptSettings(self):
        keyList = ['dropdown1', 'dropdown2', 'dropdown3', 'dropdown4', 'dropdown5']
        scriptNames = self.getScriptNames()
        scriptNames.append("---")
        # settings contains the current ScriptSettings.json data
        settings = self.getScriptSettings()
        for arg in self.argList:
            if arg is not "":
                key, value = arg.split('=')
                key = key.lower()
                for ent in keyList:
                    if key == ent:
                        # only accept the new settings string
                        # if it really is one of the scriptNames
                        if urllib.unquote(value) in scriptNames:
                            settings[ent] = value
        with open('/var/lib/crystal-signal/ScriptSettings.json', 'w+') as outfile:
                json.dump(settings, outfile)

    def getScriptSettings(self):
        path = '/var/lib/crystal-signal/ScriptSettings.json'
        if not isfile(path):
            ScriptSettingsInit = {'dropdown1': "---",
                                  'dropdown2': "---",
                                  'dropdown3': "---",
                                  'dropdown4': "---",
                                  'dropdown5': "---"}
            with open(path, 'w+') as outfile:
                json.dump(ScriptSettingsInit, outfile)
        with open(path) as data:
            return json.load(data)

    def getSettings(self):
        path = "/var/lib/crystal-signal/Settings.json"
        if not isfile(path):
            SettingsInit = {'brightness': 60,
                            'language': "none"}
            with open(path, 'w+') as outfile:
                    json.dump(SettingsInit, outfile)
        with open(path) as data:
            settingsData = json.load(data)
            if not 'language' in settingsData:
                # we need to add the new language settings dict entry
                # for all users with old settings.json files.
                settingsData['language'] = 'none'
            return settingsData

    def getBrightnessSetting(self):
        settingsDict = self.getSettings()
        tmp = settingsDict['brightness']
        if tmp <= 255 and tmp >= 0:
            return tmp
        elif tmp > 255:
            return 255
        else:
            return 0
        return settingsDict['brightness']

    def getLanguageSetting(self):
        tmp = self.getSettings()
        return tmp['language']

    def getAvailableLanguages(self):
        path = "/var/www/html/languageFiles"
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        fileNamesWithoutEndings = []
        for ent in onlyfiles:
            fileNamesWithoutEndings.append(splitext(ent)[0])
        return fileNamesWithoutEndings

    def setSettings(self):
        path = "/var/lib/crystal-signal/Settings.json"
        # sets one Settings entry (parameter-value pair in self.argList)
        keyList = ['brightness', 'language']
        # settings contains the current Settings.json data
        settings = self.getSettings()
        for arg in self.argList:
            if arg is not "":
                key, value = arg.split('=')
                key = key.lower()
                for ent in keyList:
                    if key == ent:
                        try: # Test weather or not the thing can be converted to an int
                            settings[ent] = int(value)
                        except ValueError:
                            # the value must be a string then
                            settings[ent] = value
        with open(path, 'w+') as outfile:
            json.dump(settings, outfile)

# - - - - - - - - - - - - - - - - -
# SETTING UP SOCKET & CONTROLLER  -
# - - - - - - - - - - - - - - - - -
# Socket
server = ThreadedTCPServer(('localhost', 7777), ThreadedTCPRequestHandler, False)
server.allow_reuse_address = True
server.server_bind()
server.server_activate()
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()
# LEDController
ledCtrl = LEDController()

# - - - - - - - - - - - - - - - -
# - - - - - MAIN LOOP - - - - - -
# - - - - - - - - - - - - - - - -
while True:
    try:
        ledCtrl.update()
    except(KeyboardInterrupt, SystemExit):
        server.shutdown()
        server.server_close()
        raise
    except:
        raise

# - - - - - - - - - - - - - - - -
# - - - - - - MEMO  - - - - - - -
# - - - - - - - - - - - - - - - -

