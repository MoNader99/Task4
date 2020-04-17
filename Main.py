from PyQt5 import QtWidgets , QtCore
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QUrl, QDirIterator, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QFileDialog, QAction, QHBoxLayout, QVBoxLayout, QSlider,QMessageBox
from pyqtgraph import PlotWidget, plot, PlotItem
from Gui import Ui_MainWindow
import numpy as np
import pyqtgraph as pg
import cv2
import logging
import sys
import wave
import pyaudio
import os
import sounddevice as sd


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        pg.setConfigOption('background', 'w')

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.Input_X_1=0
        self.Input_Y_1=0
        self.Input_X_2=0
        self.Input_Y_2=0
        self.durationF_1=0
        self.durationF_2=0


        self.mixedArray_Y=[]
        self.mixedArray_X=[]
        self.mixedArray_Duration=[]
        

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
            # x.setMouseEnabled(x=False, y=False)
            pass
        #------------------
    #----------------------------------------------------------------------------------------------------------------
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
                        self.ui.Play_1.clicked.connect(lambda : self.Play(self.Input_Y_1[0],self.durationF_1))
                        self.plot(self.graphic_View_Array[0],self.Input_X_1,self.Input_Y_1[0])
                        QMessageBox.warning(self,'Warning',"First Song", QMessageBox.Ok )
                    if num==1:
                        self.Input_X_2=self.X_Y_Data[0]
                        self.Input_Y_2=self.X_Y_Data[1]
                        self.ui.Play_2.clicked.connect(lambda : self.Play(self.Input_Y_2[0],self.durationF_2))
                        self.plot(self.graphic_View_Array[1],self.Input_X_2,self.Input_Y_2[0])
                        QMessageBox.warning(self,'Warning',"Second Song", QMessageBox.Ok )


                         
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
        # if self.Input_Y_1!=0 and self.Input_Y_2!=0:
        QMessageBox.warning(self,'Warning',"Next Update ya ray2", QMessageBox.Ok )
        userChoice=self.ui.SelectedSong.currentText()
        value= (self.ui.MixerSlider.value())/10
        print(value)
        print(userChoice)
        # if(userChoice=="First_Song"):
        #     self.mixedArray_X=(value*self.Input_X_1)+((1-value)*self.Input_X_2)
        #     self.mixedArray_Y=(value*self.Input_Y_1)+((1-value)*self.Input_Y_2)
        #     self.mixedArray_Duration=(value*self.durationF_1)+((1-value)*self.durationF_2)
        # elif(userChoice=="Second_Song"):
        #     self.mixedArray_X=(value*self.Input_X_2)+((1-value)*self.Input_X_1)
        #     self.mixedArray_Y=(value*self.Input_Y_2)+((1-value)*self.Input_Y_1)
        #     self.mixedArray_Duration=(value*self.durationF_2)+((1-value)*self.durationF_1)

        # self.ui.Play_Mix.clicked.connect(lambda : self.Play(self.mixedArray_Y[0],self.mixedArray_Duration))

            
    #------------------------------------------------------------------------------------------------------------------------

    def plot(self,graph,X,Y):
        ModMin = np.nanmin(Y)
        ModMax = np.nanmax(Y)
        graph.clear()
        graph.setXRange(X[0],X[-1])
        graph.plotItem.getViewBox().setLimits(xMin=X[0], xMax=X[-1], yMin=ModMin- ModMin * 0.1, yMax=ModMax + ModMax* 0.1)
        graph.plot(X,Y,pen='r')


    #------------------------------------------------------------------------------------------------------------------------

    #------------------------------------------------------------------------------------------------------------------------      
    def Play(self,array,D):
        if ((len(self.Input_X_1) != 0 and len(self.Input_Y_1) != 0) or ((len(self.Input_X_2) != 0 and len(self.Input_Y_2) != 0))):
            sd.play(array,len(array)/D)
        else:
            pass

    
    def Stop(self):
        if ((len(self.Input_X_1) != 0 and len(self.Input_Y_1) != 0) or ((len(self.Input_X_2) != 0 and len(self.Input_Y_2) != 0))):
            sd.stop()
        else:
            pass
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