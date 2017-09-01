#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import threading
import time
from subprocess import call, Popen, PIPE, STDOUT
from os.path import isfile, join
from os import listdir
import json

# - - - - - - - - - - - - - - - - - -
# - -  TALK MESSAGE CONTROLLER  - - -  
# - - - - - - - - - - - - - - - - - - 
class SpeakMessageController:

    def __init__(self, path):
        self.audioFilePath = path

    def createAndPlayAudio(self, audioString):
        args = ["open_jtalk", "-m", 
                "/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice", 
                "-x", "/var/lib/mecab/dic/open-jtalk/naist-jdic", "-ow", 
                self.audioFilePath]
        self.popenAndCall(self.onFinishJTalk, args, audioString)

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

# - - - - - - - - - - - - - - - - 
# - - - - - TEST AREA - - - - - -
# - - - - - - - - - - - - - - - -
#speakMessageController = SpeakMessageController();
#speakMessageController.createAndPlayAudio("みあああああう");

