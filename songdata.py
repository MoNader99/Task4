from PyQt5 import QtWidgets , QtCore
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QUrl, QDirIterator, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, QAction, QHBoxLayout, QVBoxLayout, QSlider,QMessageBox
from pyqtgraph import PlotWidget, plot, PlotItem
from Gui import Ui_MainWindow
import numpy as np
import pyqtgraph as pg
import logging
import sys
import wave
import os
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import pylab
from skimage.feature import peak_local_max
import imagehash as ih
from PIL import Image

class song_data():
    def __init__(self):
        self.song_name = None
        self.song_index = None

        self.spectro_path = None
        self.Spectrogram = None
        self.Frequency = None

        self.perceptualHashArray = None
        self.peaksFeature = None
        self.peaksFeatureFrequencyActualValues = None
        self.peaksTimeDifferenceFeature = None

        self.song_data = None
        self.frameRate = None
        
    def set_Data(self, filepath, index):
        if filepath != None:
            self.spectro_path = filepath
            self.song_index = index

            self.generate_spectro()

    #------------------------------------------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------------------------------------------

    def generate_spectro(self):
        head , tail = os.path.split(self.spectro_path)

        self.song_name = tail

        wav = wave.open(self.spectro_path, 'r')
        frames = wav.readframes(-1)
        sound_info = pylab.fromstring(frames, 'int16')
        frame_rate = wav.getframerate()
        wav.close()
        
        sound_info = sound_info[0 : 60 * frame_rate]

        if self.song_data == None:
            self.song_data = sound_info
            self.frameRate = frame_rate


        pylab.figure(num=None, figsize=(19, 12))
        pylab.subplot(111)
        spectrum , freqs , time , image = pylab.specgram(sound_info, Fs=frame_rate)
        self.Spectrogram , self.Frequency = spectrum , freqs

        self.spectro_path = self.spectro_path + ' Spectrogram' +str(self.song_index)+'.png'
        pylab.savefig(self.spectro_path, bbox_inches='tight')

        self.perceptualHash(self.spectro_path)
        self.peakFeaturesGenerate()
        
    def GenerateData_NoFilePath(self): 
        
        pylab.figure(num=None, figsize=(19, 12))
        pylab.subplot(111)
        spectrum , freqs , time , image = pylab.specgram(self.song_data, Fs=self.frameRate)
        self.Spectrogram , self.Frequency = spectrum , freqs

        pylab.savefig('Mixed Spectrogram.png',bbox_inches='tight')
        pylab.close()
        self.spectro_path = 'Mixed Spectrogram.png'

        #Generating Extra data
        self.perceptualHash(self.spectro_path)
        self.peakFeaturesGenerate()
    #------------------------------------------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------------------------------------------

    def perceptualHash(self,filepath):
        spectrogramImage = Image.open(filepath)
        self.perceptualHashArray = ih.phash(spectrogramImage)
    
    def peakFeaturesGenerate(self):  
        min_freq = 0
        max_freq = 15000

        Z1, self.Frequency = self.cut_specgram(min_freq, max_freq, self.Spectrogram, self.Frequency)

        coordinates = peak_local_max(Z1, min_distance=20, threshold_abs=20)

        self.peaksFeature = coordinates
        
        self.peaksFeatureFrequencyActualValues = coordinates[:,1]

        #Generate time difference after generating the peaks
        self.peaksTimeDifferenceFeatureGenerate()
    
    def peaksTimeDifferenceFeatureGenerate(self):
        #indexes for moving in array
        rows, cols = self.peaksFeature.shape
        i = 0
        j = 1
        test = [ ]
        #----------------

        if len(self.peaksFeature) == 0:
            print("No peaks detected")
        else:
            for i in range(len(self.peaksFeature)):
                try:
                    value = self.peaksFeature[i,0] - self.peaksFeature[j,0]
                    if value != 0:
                        test.append(value)
                    j = j + 1
                    i = i + 1

                except:
                    print("created a spectrogram")

        self.peaksTimeDifferenceFeature = np.array(test)
        print(self.peaksTimeDifferenceFeature)

    def compareHashes(self,comparedSong):
        output = (self.perceptualHashArray - comparedSong.perceptualHashArray) / 64 #Returns percentage of how different they are, in decimal not percent
        
        return (1-output)

    def cut_specgram(self,min_freq, max_freq, spec, freqs):
        spec_cut = spec[(freqs >= min_freq) & (freqs <= max_freq)]
        freqs_cut = freqs[(freqs >= min_freq) & (freqs <= max_freq)]
        Z_cut = 10.0 * np.log10(spec_cut)
        Z_cut = np.flipud(Z_cut)
        return Z_cut, freqs_cut

    #------------------------------------------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------------------------------------------
    
    def comparePeakFeaturesGenerateDifference(self,comparedSong):
        percenatge = 0
        multiplySum = 1 
        percentArr = []
        
        check = False
        try:
            max1 = max(self.peaksFeatureFrequencyActualValues)
            max2= max(comparedSong.peaksFeatureFrequencyActualValues)
        except:
            return 0
        compareOne = (self.peaksFeature)/ (max1/100)
        compareTwo = (comparedSong.peaksFeature)/ (max2/100) 
        
        for i in range (len(self.peaksFeatureFrequencyActualValues)):
            check = False
            for j in range (len(comparedSong.peaksFeatureFrequencyActualValues)):
                
                if (self.peaksFeature[i][0]==comparedSong.peaksFeature[j][0]):
                    check = True
                    if (self.peaksFeature[i][1]==comparedSong.peaksFeature[j][1]):
                        percentArr.append(1)
                    else:
                        freqCompare = (1- abs((compareOne[i][1]-compareTwo[j][1])/100))
                    
                else:
                    if (check == False and j == (len(compareTwo)-1)):
                        percentArr.append(0)
                        break
                    elif(len(compareTwo)-1 == j):
                        break
        if (len(percentArr)==0):
           percentArr=np.zeros(len(comparedSong.peaksFeatureFrequencyActualValues))
        
        return np.nanmean(percentArr)
               


    def comparePeaksTimeDifferenceFeatureGenerateDifference(self,comparedSong):
        result_multiply_percentages = 1
        if len(self.peaksTimeDifferenceFeature) < len(comparedSong.peaksTimeDifferenceFeature):
            compared_array = self.peaksTimeDifferenceFeature
        else:
            compared_array = comparedSong.peaksTimeDifferenceFeature

        output = np.zeros(len(compared_array))
        percentages = np.zeros(len(compared_array))
        max1 = max(self.peaksTimeDifferenceFeature)
        max2=max(comparedSong.peaksTimeDifferenceFeature)
        compareOne = (self.peaksTimeDifferenceFeature)/ (max1/100)
        compareTwo = (comparedSong.peaksTimeDifferenceFeature)/ (max2/100) 
        compareOne=compareOne[0:(len(compared_array))]
        compareTwo=compareTwo[0:(len(compared_array))]
        for i in range(len(compared_array)):
            output[i] = (1-abs(compareOne[i] - compareTwo[i])/100)
            
            if output[i] == 0:
                percentages[i] = 1
        result_multiply_percentages = np.nanmean(output)
            
        return result_multiply_percentages
    
    def mixSongAmplitude(self,comparedSong,sliderValue,newSong):
        
        newSong.songSoundData = self.song_data * sliderValue + comparedSong.songSoundData * (1-sliderValue)

        an_array = np.array(newSong.songSoundData, dtype=np.float64)
        newSong.songSoundData = an_array.astype(np.int16)
        
        newSong.frameRate = self.frameRate
        newSong.GenerateData_NoFilePath()