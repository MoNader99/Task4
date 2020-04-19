from PyQt5 import QtWidgets , QtCore
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QUrl, QDirIterator, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, QAction, QHBoxLayout, QVBoxLayout, QSlider,QMessageBox
from pyqtgraph import PlotWidget, plot, PlotItem
from Gui import Ui_MainWindow
import numpy as np
import pyqtgraph as pg
import matplotlib.pyplot as plt
import logging
import sys
import wave
import pydub
import pyaudio
import os
import sounddevice as sd



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        pg.setConfigOption('background', 'w')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.Song1 = []
        self.Song2 = []
        
        self.mixedArray = []

        self.Input_X_1=0
        self.Input_Y_1=0
        self.Input_X_2=0
        self.Input_Y_2=0
        self.durationF_1=0
        self.durationF_2=0
        
        LOG_FILENAME = 'LOGFILE.txt'
        file = open(LOG_FILENAME,"r+")
        file.truncate(0)
        file.close()

        logging.basicConfig(filename=LOG_FILENAME,format='%(asctime)s - %(message)s ',datefmt='%d-%b-%y %H:%M:%S',level=logging.INFO)

    #----------------------------------------------------------------------------------------------------------------
        self.graphic_View_Array=[self.ui.Spectrogram_1,self.ui.Spectrogram_2]
        for x in self.graphic_View_Array:
            # x.getPlotItem().hideAxis('bottom')
            # x.getPlotItem().hideAxis('left')
            x.setMouseEnabled(x=False, y=False)
            pass
        #------------------

        self.playArray=[self.ui.Play_1,self.ui.Play_2]
    #----------------------------------------------------------------------------------------------------------------
        self.browseArray=[self.ui.BrowseButton,self.ui.BrowseButton_2]
        self.ui.BrowseButton.clicked.connect(lambda : self.Import(0))
        self.ui.BrowseButton_2.clicked.connect(lambda : self.Import(1))
    #----------------------------------------------------------------------------------------------------------------
        self.ui.MixerSlider.sliderReleased.connect(self.ValueChanged)
    #----------------------------------------------------------------------------------------------------------------
        self.stopArray=[self.ui.Stop_Button,self.ui.Stop_Button_2]
        for x in self.stopArray:
            x.clicked.connect(self.Stop)
    #----------------------------------------------------------------------------------------------------------------

    def Import(self,num):
        filePaths = QtWidgets.QFileDialog.getOpenFileNames(self, 'Multiple File',"~/Desktop",'*.mp3 && *.wav')
        for filePath in filePaths:
            for f in filePath: 
                if f == "*" or f == None:
                    break
                ext = os.path.splitext(f)[-1].lower()  # Check file extension  

                if ext == ".wav":
                    self.X_Y_Data = self.ReadFromWav(f,num)
                    if num==0:
                        self.Input_X_1=self.X_Y_Data[0]
                        self.Input_Y_1=self.X_Y_Data[1]
        
                    if num==1:
                        self.Input_X_2=self.X_Y_Data[0]
                        self.Input_Y_2=self.X_Y_Data[1]

                    print(self.Input_Y_1, self.Input_Y_2)   

                if ext == ".mp3" :
                    pydub.AudioSegment.converter = r"C:\ffmpeg\ffmpeg\bin\ffmpeg.exe"
                    songFile = pydub.AudioSegment.from_mp3(f)
                    if num==0:
                        self.Song1 = np.array(songFile.get_array_of_samples())
                        self.Song1 = self.Song1.reshape((-1, 2))
                        self.Song1 = self.Song1.flatten()
                        self.ui.Play_1.clicked.connect(lambda : self.Play(self.Song1))
                        logging.info('User Imported from Browse 1')
                    if num==1:
                        self.Song2 = np.array(songFile.get_array_of_samples())
                        self.Song2 = self.Song2.reshape((-1, 2))
                        self.Song2=self.Song2.flatten()
                        self.ui.Play_2.clicked.connect(lambda : self.Play(self.Song2))
                        logging.info('User Imported from Browse 2')

                    
                    print(self.Song1, self.Song2)    

                        
   #----------------------------------------------------------------------------------------------------------------

    def ReadFromWav(self,file,num):  

        p = pyaudio.PyAudio()
        self.waveFile = wave.open(file,'rb')

        self.format = p.get_format_from_width(self.waveFile.getsampwidth())
        channel = self.waveFile.getnchannels()
        self.rate = self.waveFile.getframerate()
        self.frame = self.waveFile.getnframes()
        self.stream = p.open(format=self.format,  # DATA needed for streaming
                            channels=channel,
                            rate=self.rate,
                            output=True)
        if num==0:
            self.durationF_1 = self.frame / float(self.rate) # For playing the sound

        if num==1:
            self.durationF_2 = self.frame / float(self.rate) # For playing the sound

        self.data_int = self.waveFile.readframes(self.frame)
        self.data_plot = np.fromstring(self.data_int, 'Int16')
        self.data_plot.shape = -1, 2

        self.data_plot = self.data_plot.T
        self.time = np.arange(0, self.frame) * (1.0 / self.rate)

        return self.time,self.data_plot

    #------------------------------------------------------------------------------------------------------------------------
    def ValueChanged(self):
        if len(self.Song2)!=0 and len(self.Song1)!=0:
            userChoice=self.ui.SelectedSong.currentText()
            value= (self.ui.MixerSlider.value())/10
            if(userChoice=="First_Song"):
                if len(self.Song1) > len(self.Song2):
                    self.mixedArray=(self.Song1[0:len(self.Song2)]*value)+(self.Song2*(1-value))
                else:
                    self.mixedArray=(self.Song1*value)+(self.Song2[0:len(self.Song1)]*(1-value))
                
            elif(userChoice=="Second_Song"):
                if len(self.Song1) > len(self.Song2):
                    self.mixedArray=(self.Song2[0:len(self.Song1)]*value)+(self.Song1*(1-value))
                else:
                    self.mixedArray=(self.Song2*value)+(self.Song1[0:len(self.Song2)]*(1-value))
                    
            self.ui.Play_Mix.clicked.connect(lambda : self.Play(self.mixedArray))
            logging.info('User Created a mix ')
        else:
            QMessageBox.warning(self,'Warning',"ADD TWO SONGS", QMessageBox.Ok )
            logging.info('User tried to Create a mix while there is No 2 Songs imported')
        
    #------------------------------------------------------------------------------------------------------------------------      
    def Play(self,array):    
        sd.play(array)

    
    def Stop(self):
        sd.stop()
    #------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

#////////////////////////////// Main /////////////////////////////////////

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()

if __name__ == "__main__":
    main()