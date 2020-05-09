from PyQt5 import QtWidgets , QtCore, QtGui
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
from songdata import song_data


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        pg.setConfigOption('background', 'w')
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.Song1 = []
        self.Song2 = []
        
        self.mixedArray = []
        self.mixedArray_Duration=0

        self.mixedsong = song_data()

        self.songsArray = []
        self.song_index = 0

        self.Ext_1=None
        self.Ext_2=None
        
        self.Input_X_1=[]
        self.Input_Y_1=[]
        self.Input_X_2=[]
        self.Input_Y_2=[]
        self.durationF_1=0
        self.durationF_2=0

        self.similarityIndex = []
        self.similarityIndexID = []
        self.topTenSimilarityIndex = []
        
        LOG_FILENAME = 'LOGFILE.txt'
        file = open(LOG_FILENAME,"r+")
        file.truncate(0)
        file.close()

        self.generate_spectrograms()

        logging.basicConfig(filename=LOG_FILENAME,format='%(asctime)s - %(message)s ',datefmt='%d-%b-%y %H:%M:%S',level=logging.INFO)

    #----------------------------------------------------------------------------------------------------------------
        self.graphic_View_Array=[self.ui.Spectrogram_1,self.ui.Spectrogram_2]
        for x in self.graphic_View_Array:
            x.setMouseEnabled(x=False, y=False)
            pass
        #------------------

        self.playArray=[self.ui.Play_1,self.ui.Play_2]
    #----------------------------------------------------------------------------------------------------------------
        self.browseArray=[self.ui.BrowseButton,self.ui.BrowseButton_2]
        self.ui.BrowseButton.clicked.connect(lambda : self.Import(0))
        self.ui.BrowseButton_2.clicked.connect(lambda : self.Import(1))
        self.ui.GenerateButton.clicked.connect(self.start_compare)
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
                        self.Ext_1=ext
                        self.Input_X_1=self.X_Y_Data[0]
                        self.Input_Y_1=self.X_Y_Data[1]
                        self.ui.Play_1.clicked.connect(lambda : self.Play_Wav(self.Input_Y_1[0],self.durationF_1))
                        logging.info('User Imported wav file from Browse 1')
        
                    if num==1:
                        self.Ext_2=ext
                        self.Input_X_2=self.X_Y_Data[0]
                        self.Input_Y_2=self.X_Y_Data[1]
                        self.ui.Play_2.clicked.connect(lambda : self.Play_Wav(self.Input_Y_2[0],self.durationF_2))
                        logging.info('User Imported wav file from Browse 2')

                if ext == ".mp3" :
                    
                    pydub.AudioSegment.converter = r"C:\ffmpeg\ffmpeg\bin\ffmpeg.exe"
                    songFile = pydub.AudioSegment.from_mp3(f)
                    if num==0:
                        self.Ext_1=ext
                        self.Song1 = np.array(songFile.get_array_of_samples())
                        self.Song1 = self.Song1.reshape((-1, 2))
                        self.ui.Play_1.clicked.connect(lambda : self.Play(self.Song1))
                        logging.info('User Imported mp3 file from Browse 1')
                    if num==1:
                        self.Ext_2=ext
                        self.Song2 = np.array(songFile.get_array_of_samples())
                        self.Song2 = self.Song2.reshape((-1, 2))
                        self.ui.Play_2.clicked.connect(lambda : self.Play(self.Song2))
                        logging.info('User Imported mp3 file from Browse 2')
      
   #----------------------------------------------------------------------------------------------------------------
                        
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

    #------------------------------------------------------------------------------------------------------------------------
    def ValueChanged(self):
        userChoice=self.ui.SelectedSong.currentText()
        value= (self.ui.MixerSlider.value())/10
        self.mixedArray=[]

        if (self.Ext_1==self.Ext_2) and (self.Ext_2==".mp3"):
            if len(self.Song2)!=0 and len(self.Song1)!=0:
                if(userChoice=="First_Song"):
                    if len(self.Song1) >= len(self.Song2):
                        self.mixedArray=((self.Song1[0:len(self.Song2)]*value)+(self.Song2*(1-value)))/10000
                    else:
                        self.mixedArray=((self.Song1*value)+(self.Song2[0:len(self.Song1)]*(1-value)))/10000
                    
                elif(userChoice=="Second-Song"):
                    if len(self.Song2) >= len(self.Song1):
                        self.mixedArray=((self.Song2[0:len(self.Song1)]*value)+(self.Song1*(1-value)))/10000
                    else:
                        self.mixedArray=((self.Song2*value)+(self.Song1[0:len(self.Song2)]*(1-value)))/10000
                        
                self.ui.Play_Mix.clicked.connect(lambda : self.Play(self.mixedArray))
                logging.info('User Created a mix with mp3 files ')
            else:
                QMessageBox.warning(self,'Warning',"ADD TWO SONGS", QMessageBox.Ok )
                logging.info('User tried to Create a mix while there is No 2 Songs imported')

        elif (self.Ext_1==self.Ext_2) and (self.Ext_2==".wav") :
            if len(self.Input_Y_1)!=0 and len(self.Input_Y_2)!=0:
                if(userChoice=="First_Song"): 
                    if len(self.Input_Y_1[0]) >= len(self.Input_Y_2[0]):
                        self.mixedArray.append(((self.Input_Y_1[0][0:len(self.Input_Y_2[0])]*value)+(self.Input_Y_2[0]*(1-value)))/10000)
                        self.mixedArray.append(((self.Input_Y_1[1][0:len(self.Input_Y_2[1])]*value)+(self.Input_Y_2[1]*(1-value)))/10000)
                        self.mixedArray_Duration=self.durationF_1
                    else:
                        self.mixedArray.append(((self.Input_Y_1[0]*value)+(self.Input_Y_2[0][0:len(self.Input_Y_1[0])]*(1-value)))/10000)
                        self.mixedArray.append(((self.Input_Y_1[1]*value)+(self.Input_Y_2[1][0:len(self.Input_Y_1[1])]*(1-value)))/10000)
                        self.mixedArray_Duration=self.durationF_2
                elif(userChoice=="Second-Song"):
                    if len(self.Input_Y_2[0]) >= len(self.Input_Y_1[0]):
                        self.mixedArray.append(((self.Input_Y_2[0][0:len(self.Input_Y_1[0])]*value)+(self.Input_Y_1[0]*(1-value)))/10000)
                        self.mixedArray.append(((self.Input_Y_2[1][0:len(self.Input_Y_1[1])]*value)+(self.Input_Y_1[1]*(1-value)))/10000)
                        self.mixedArray_Duration=self.durationF_2
                    else:
                        self.mixedArray.append(((self.Input_Y_2[0]*value)+(self.Input_Y_1[0][0:len(self.Input_Y_2[0])]*(1-value)))/10000)
                        self.mixedArray.append(((self.Input_Y_2[1]*value)+(self.Input_Y_1[1][0:len(self.Input_Y_2[1])]*(1-value)))/10000)
                        self.mixedArray_Duration=self.durationF_1
                        
                self.ui.Play_Mix.clicked.connect(lambda : self.Play_Wav(self.mixedArray[0],self.mixedArray_Duration))
                logging.info('User Created a mix with wav files ')

                self.mixedsong.song_data = self.mixedArray
        else:
            QMessageBox.warning(self,'Warning',"add songs with the same extension", QMessageBox.Ok )
            logging.info('User tried to Create a mix while the two songs is not the same extension')

    #------------------------------------------------------------------------------------------------------------------------
            
    #------------------------------------------------------------------------------------------------------------------------      
    def Play(self,array):    
        sd.play(array)

    def Play_Wav(self,array,D):
        if ((len(self.Input_X_1) != 0 and len(self.Input_Y_1) != 0) or ((len(self.Input_X_2) != 0 and len(self.Input_Y_2) != 0))):
            sd.play(array,len(array)/D)
        else:
            pass
    
    def Stop(self):
        sd.stop()
    #------------------------------------------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------------------------------------------

    def generate_spectrograms(self):
        path = '/Songs'
        filepaths = [os.path.join(r,file) for r,d,f in os.walk(os.getcwd() + path) for file in f]
        filepaths = [x for x in filepaths if x.endswith(".wav")]
        for f in filepaths:
            tempSong = song_data()
            tempSong.set_Data(f,self.song_index)
            self.songsArray.append(tempSong)
            self.song_index = self.song_index + 1
    
    #------------------------------------------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------------------------------------------

    def start_compare(self):
        for i in range(len(self.songsArray)):
            print(len(self.songsArray))
            percent_hashes = self.mixedArray.compareHashes(self.songsArray[i])
            percent_peaks = self.mixedArray.comparePeakFeaturesGenerateDifference(self.songsArray[i])

            tempSimilarityIndex = (percent_hashes + percent_peaks )/2
            self.similarityIndex.append(tempSimilarityIndex * 100)
            self.similarityIndexID.append(self.songsArray[i].songID)


        tempSimilarityIndex = self.similarityIndex
        print("---------------------------------")
        print(self.similarityIndexID)
        print(self.similarityIndex)
        print("---------------------------------")

        numpyArr=np.array(self.similarityIndex) 
        self.TopTenSimilarIDs=numpyArr.argsort()[::-1]

        tempSimilarityIndex.sort(reverse = True)

        if len(tempSimilarityIndex) < 10 :
            for i in tempSimilarityIndex:
                self.topTenSimilarityIndex.append(i)
        else:
            for i in range(10):
                self.topTenSimilarityIndex.append(tempSimilarityIndex[i])
        print("Top Similar IDs")
        print (self.TopTenSimilarIDs)
        print(self.topTenSimilarityIndex)

        for i in range(len(self.topTenSimilarityIndex)):
            self.Fill_Similarity_Table(self.TopTenSimilarIDs[i],i)

        self.topTenSimilarityIndex = [ ]
        self.similarityIndex = [ ]
        self.similarityIndexID = [ ]

    #------------------------------------------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------------------------------------------

    def Fill_Similarity_Table(self,songIndex,normalIndex):
        rowPosition = self.ui.SongsTable.rowCount()
        self.ui.SongsTable.insertRow(rowPosition)
        numrows = self.ui.SongsTable.rowCount()           
        self.ui.SongsTable.setRowCount(numrows)
        self.ui.SongsTable.setColumnCount(2)           
        self.ui.SongsTable.setItem(numrows - 1, 0 ,QtGui.QSongsTableItem(self.songsArray[songIndex].songName))
        self.ui.SongsTable.setItem(numrows - 1, 1 ,QtGui.QSongsTableItem(str(round(self.topTenSimilarityIndex[normalIndex],2))+"%"))

        self.ui.SongsTable.setHorizontalHeaderItem(0,QtGui.QSongsTableItem("Song Name"))
        self.ui.SongsTable.setHorizontalHeaderItem(1,QtGui.QSongsTableItem("Similarity Index"))

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