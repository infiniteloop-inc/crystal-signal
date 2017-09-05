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
        self.DropDownNameToFilePathDict = {
            'M001' : ['/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice', 'm'],
            'Mei (normal)' : [meiVoiceDirPath + 'mei_normal.htsvoice', 'w'],
            'Mei (happy)' : [meiVoiceDirPath + 'mei_happy.htsvoice', 'w'],
            'Mei (bashful)' : [meiVoiceDirPath + 'mei_bashful.htsvoice', 'w'],
            'Mei (angry)' : [meiVoiceDirPath + 'mei_angry.htsvoice', 'w'],
            'Mei (sad)' : [meiVoiceDirPath + 'mei_sad.htsvoice', 'w']
            }

    def getVoiceDropDownNames(self):
        tmp = []
        for key, tuple_ in self.DropDownNameToFilePathDict.items():
            tmp.append([key, tuple_[1]])
        return tmp

    def createAndPlayAudio(self, audioString, voiceName):
        voicePath = self.getFullFilePath(voiceName)
        print voicePath
        args = ["open_jtalk", 
                "-m", voicePath, 
                "-x", "/var/lib/mecab/dic/open-jtalk/naist-jdic", 
                "-ow", self.audioFilePath]
        self.popenAndCall(self.onFinishJTalk, args, audioString)

    def getFullFilePath(self, voiceName):
        if voiceName in self.DropDownNameToFilePathDict.keys():
            return self.DropDownNameToFilePathDict[voiceName][0]
        else:
            # return Mei (happy) as default if no key fits.
            return self.DropDownNameToFilePathDict['Mei (happy)'][0]

    def onFinishJTalk(self):
        call(["aplay", self.audioFilePath])

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
