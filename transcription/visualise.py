"""
NOTEPADAI
(Visualiser)

A data science tool to produce cool graphs accompanying the process of speech recognition
"""


from transcription.helper import *

import librosa
import vlc
import matplotlib.pyplot as plt
import pandas as pd

CHUNK = 320
MAX_COLUMNS = 200  # Output of Pandas DataFrames


class Visualise:
    def __init__(self, path, tsv=None):
        if path[-4:] == ".mp3":
            self.path = path
            self.id = path[-132:-4]
        else:
            self.path = path + ".mp3"
            self.id = path

        self.data, self.sample_rate = librosa.load(path)
        self.__player__ = vlc.MediaPlayer(path)
        if tsv is not None:
            pd.options.display.max_colwidth = MAX_COLUMNS
            table = pd.read_csv(tsv, sep='\t')
            self.metadata = pd.DataFrame(table.query("path == @self.id"))

    def play(self):
        self.__player__.play()
        self.__player__ = vlc.MediaPlayer(self.path)

    def phonemes(self):
        return split_spellings(str(self.metadata["sentence"].str.get_dummies()))

    def as_mfcc_stream(self, chunk=CHUNK):
        for window in audio_to_stream(self.data, chunk):
            yield librosa.feature.mfcc(window)

    def as_audio_stream(self, chunk=CHUNK):
        return audio_to_stream(self.data, chunk)


def bar_graph(column):
    categories = {}
    for value in column:
        if value in categories:
            categories[value] += 1
        else:
            categories.update({value: 1})
    bar = pd.DataFrame({'value': list(categories.keys()), 'val': list(categories.values())})
    bar.plot.barh(x='value', y='val', rot=0)


def specgram(obj, xlabel=None, ylabel=None, axis=None, chunk=CHUNK):
    s = plt
    s.specgram(obj.data, NFFT=chunk, Fs=obj.sample_rate)

    if xlabel is not None:
        s.xlabel(xlabel)
    if ylabel is not None:
        s.ylabel(ylabel)
    if axis is not None:
        s.axis(axis)

    s.show()

