import sys
from PySide2 import QtWidgets, QtCore
import pyqtgraph as pg
import audio_notes
import numpy as np
import time
from audio import chroma_detection

class app():
    def __init__(self):
        self.fps = 60
        self.x = np.zeros(1)
        self.y = np.zeros(1)
        self.start_time = None
        self.district = 30
        self.audiodic, self.audio_times, self.audio_notes = audio_notes.get()
        self.chroma_detection = chroma_detection()

        self.app = QtWidgets.QApplication([])
        self.win = pg.GraphicsLayoutWidget()
        self.plotitem = self.win.addPlot(title=self.audiodic["name"])

        self.y_min = self.audio_notes.min() - 2
        self.y_max = self.audio_notes.max() + 2
        self.plotitem.setXRange(-self.district/2, self.district/2)
        self.plotitem.setYRange(self.y_min, self.y_max)
        self.plotitem.showGrid(x=False, y=False)

        self.division_plot = self.plotitem.plot(pen=pg.mkPen(color="w", width=2.5,))
        self.audio_plot = self.plotitem.plot(pen=None, symbol="s", symbolSize=5, symbolPen="g",symbolBrush="g")
        self.plot = self.plotitem.plot(pen=None, symbol="s", symbolSize=5, symbolPen="w",symbolBrush="w")
        self.audio_plot.setData(self.audio_times, self.audio_notes)

    def update(self):

        chroma = self.chroma_detection.get_chroma(self.indata)

        if chroma != None:
            # 補正
            index = np.where(self.now <= self.audio_times)[0]
            if index.size > 0:
                chroma_adj = self.audio_notes[index.min()]//12
            else:
                chroma_adj = np.mean(self.audio_notes)//12
            chroma += 12 * chroma_adj

            self.x = np.append(self.x, self.now)
            self.y = np.append(self.y, chroma)

        self.x = self.x[-1000:]
        self.y = self.y[-1000:]

        self.plotitem.setXRange(-self.district/2 + self.now, self.district/2 + self.now)
        self.division_plot.setData((self.now, self.now), (self.y_min, self.y_max))
        self.plot.setData(self.x,self.y)

    def run(self):
        self.win.showMaximized()

        self.launch_time = time.time()
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(1000 * 1/self.fps)

        if (sys.flags.interactive != 1):
            QtWidgets.QApplication.instance().exec_()

    def callback_indata(self, indata):
        self.indata = indata

    def callback_time(self, t):
        if self.start_time == None:
            delta = time.time() - self.launch_time
            self.start_time = t + delta

        self.now = t - self.start_time