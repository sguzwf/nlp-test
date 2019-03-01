#!/usr/bin/env python3

"""
NOTEPADAI
(Processor)

Provides tools to transcript an audio stream
"""

import queue
import threading
import numpy
import pyaudio


class Processor (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.samples = queue.Queue
        self.response = queue.Queue
        self.isRunning = False

    def run(self):
        self.isRunning = True
        while self.isRunning and not self.samples.empty:
            # TODO: Add the actual audio processing here
            # (Take bytes from samples queue, process them, put words into other response queue)
            pass

    def stop(self):
        self.isRunning = False