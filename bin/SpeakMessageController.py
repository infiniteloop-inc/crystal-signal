#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import threading
import time
from subprocess import call, Popen, PIPE, STDOUT
import json

# - - - - - - - - - - - - - - - - - -
# - -  SPEAK MESSAGE CONTROLLER - - -  
# - - - - - - - - - - - - - - - - - - 
class SpeakMessageController:
    def __init__(self, audioPath):
        self.audioFilePath = audioPath
        meiVoiceDirPath = "/var/lib/crystal-signal/voice/mei/"
        # DropDownNameToFilePathDict is for the japanese voice files only
        self.DropDownNameToFilePathDict = {
            'M001' : ['/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice', 'm'],
            'Mei (normal)' : [meiVoiceDirPath + 'mei_normal.htsvoice', 'f'],
            'Mei (happy)' : [meiVoiceDirPath + 'mei_happy.htsvoice', 'f'],
            'Mei (bashful)' : [meiVoiceDirPath + 'mei_bashful.htsvoice', 'f'],
            'Mei (angry)' : [meiVoiceDirPath + 'mei_angry.htsvoice', 'f'],
            'Mei (sad)' : [meiVoiceDirPath + 'mei_sad.htsvoice', 'f']
            }
        # DropDownNameToOptionDict is used for the espeak plugin (e.g. english) 
        self.DropDownNameToOptionDict = {
            'f1' : ['f1', 'f'],
            'f2' : ['f2', 'f'],
            'f3' : ['f3', 'f'],
            'f4' : ['f4', 'f'],
            'f5' : ['f5', 'f'],
            'm1' : ['m1', 'm'],
            'm2' : ['m2', 'm'],
            'm3' : ['m3', 'm'],
            'm4' : ['m4', 'm'],
            'm5' : ['m5', 'm'],
        }

    def getVoiceDropDownNames(self, language):
        # this is where we need to split the control flow
        # in respect to the current language ...
        tmp = []
        if (language == 'japanese'):
            for key, tuple_ in self.DropDownNameToFilePathDict.items():
                tmp.append([key, tuple_[1]])
                tmp.sort(key=lambda tup: tup[0])
            return tmp
        elif (language == 'english'):
            for key, tuple_ in self.DropDownNameToOptionDict.items():
                tmp.append([key, tuple_[1]])
                tmp.sort(key=lambda tup: tup[0])
            return tmp
        # how can we order this tuple list?

    def createAndPlayAudio(self, audioString, voiceName, language):
        if language == 'japanese':
            voicePath = self.getFullFilePath(voiceName)
            print voicePath
            args = ["open_jtalk", 
                    "-m", voicePath, 
                    "-x", "/var/lib/mecab/dic/open-jtalk/naist-jdic", 
                    "-ow", self.audioFilePath]
            self.popenAndCall(self.onFinishJTalk, args, audioString)
        elif language == 'english':
            print(voiceName)
            args = ["espeak", 
                    "-ven+" + voiceName, 
                    "-s120", "-g0", "-p80", 
                    "--stdin"]
            self.popenAndCall(self.onFinishEspeak, args, audioString)

    def getFullFilePath(self, voiceName):
        if voiceName in self.DropDownNameToFilePathDict.keys():
            return self.DropDownNameToFilePathDict[voiceName][0]
        else:
            # return Mei (happy) as default if no key fits.
            return self.DropDownNameToFilePathDict['Mei (happy)'][0]

    def onFinishJTalk(self):
        call(["aplay", self.audioFilePath])

    def onFinishEspeak(self):
        # Note: In the case of english/espeak, we do not need to play the audio file
        # since espeak does that for us.
        print('espeak finished')

    def popenAndCall(self, onExit, popenArgs, audioString):
        # Runs the given args in a subprocess.Popen, and then calls the function
        # onExit when the subprocess has completed.
        def runInThread(onExit, popenArgs):
            proc = Popen(popenArgs, stdout=None, stdin=PIPE, stderr=None)
            proc.communicate(input = audioString)
            proc.wait()
            onExit()
            return
        thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
        thread.start()
        return thread

# - - - - - - - - - - - - - - - - - -
# - - - - - - - MEMO  - - - - - - - -  
# - - - - - - - - - - - - - - - - - - 
