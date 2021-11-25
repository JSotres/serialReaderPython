from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import QtCore
import sys
import matplotlib.pyplot as plt
from ..qt5_ui_files.serialReaderGUI import *
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import os
import math
import random
import time
import csv
import serial
import glob
import pandas as pd

class serialReaderUI(QMainWindow):
    def __init__(self):
        super().__init__()
        #Load the UI
        self.ui = Ui_SerialReader()
        self.ui.setupUi(self)

        self.ui.pushButtonStartAcquisition.clicked.connect(self.startAcquisition)
        self.ui.pushButtonContinueAcquisition.clicked.connect(self.continueAcquisition)
        self.ui.pushButtonStopAcquisition.clicked.connect(self.stopAcquisition)
        self.ui.pushButtonClose.clicked.connect(self.closeGUI)
        self.ui.pushButtonSaveData.clicked.connect(self.saveData)
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.updateData)
        

        self.t0 = 0
        self.t = []
        self.signal = []

        self.curve = self.ui.mplWidget.plot(self.t, self.signal)
        self.ui.mplWidget.setLabels(bottom='Time (s)', left='Signal', right='Signal')

        self.ui.lineEditPort.setText('COM3')
        self.ui.comboBoxBaudRate.setCurrentIndex(9)

        self.ui.comboBoxPort.addItems(self.serial_ports())
        self.ui.comboBoxPort.currentIndexChanged.connect(self.displayPort)

        self.show()

    def displayPort(self):
        self.ui.lineEditPort.setText(
            self.ui.comboBoxPort.itemText(
                self.ui.comboBoxPort.currentIndex()
            )
        )

    def startAcquisition(self):
        self.t0 = time.time()
        self.signal = []
        self.t = []
        self.port = self.ui.lineEditPort.text()
        self.baudRate = int(self.ui.comboBoxBaudRate.itemText(self.ui.comboBoxBaudRate.currentIndex()))

        print(self.serial_ports())
        self.timer.start()


    def continueAcquisition(self):
        self.timer.start()

    def updateData(self):
        self.t.append(time.time()-self.t0)
        self.signal.append(random.random())
        self.curve.setData(self.t, self.signal)
        self.ui.labelSignal.setNum(self.signal[-1])

    def stopAcquisition(self):
        self.timer.stop()            
        

    def closeGUI(self):
        QApplication.instance().quit()

    def saveData(self):
        caption = "Save File"
        directory = os.getcwd()
        filter_mask = "All Files (*)"
        name = QFileDialog.getSaveFileName(self, caption, directory, filter_mask)
        """
        with open(name[0], 'w') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerows(zip(self.t,self.signal))
        f.close()"""
        dict = {'time': self.t, 'signal':self.signal}
        df = pd.DataFrame(dict)
        df.to_csv(name[0], index=False)

    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        print(ports)
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
