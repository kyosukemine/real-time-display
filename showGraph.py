# ================================================================
# ================================================================
# API-AIO(WDM)
# MultiAiサンプル
#                                                CONTEC Co., Ltd.
# ================================================================
# ================================================================
# import matplotlib.pyplot as plt
import ctypes
import ctypes.wintypes
import sys
# import caio
# import keyboard
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from time import time
from src import AIO_160802GY_USB
import threading


class main():
    def __init__(self):
        self.AIO = AIO_160802GY_USB.AIO_160802GY_USB("AIO000", AiChannels=2)
        self.V = [np.empty(0) for i in range(self.AIO.AiChannels)]
        P = []
        self.curves = []
        self.T = np.empty(0)
        # self.V = []
        self.cnt = int()
        self.AiSamplingCount = 0

        # ----------------------------------------
        # グラフウィンドウ作成
        # ----------------------------------------
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.app = pg.mkQApp("Plotting Example")
        # mw = QtWidgets.QMainWindow()
        # mw.resize(800,800)

        self.win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
        self.win.resize(1000, 600)
        self.win.setWindowTitle('pyqtgraph example: Plotting')


        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        for i in range(self.AIO.AiChannels):
            p = self.win.addPlot(title=f"[{i}]real-time plot")
            self.curve = p.plot(pen='black')
            p.setRange(yRange=(-2, 2))
            P.append(p)
            self.curves.append(self.curve)
            self.win.nextRow()
        self.app.processEvents()
        self.TIMERANGE = 1 * 1000
        cnt = 0
        V = [np.empty(0) for i in range(self.AIO.AiChannels)]
        self.frg = False

        ptr = 0
        # ----------------------------------------
        # サンプリングスタート
        # ----------------------------------------
        self.AIO.AioStartAi()
        update_thread = threading.Thread(target=self.update, name='update')
        fft_thread = threading.Thread(target=self.fft, name='fft')
        update_thread.start()
        fft_thread.start()
        try:
            while self.win.isVisible():
                if self.frg:
                    self.app.processEvents()
                    self.frg = False
                pass
            self.AiSamplingCount = self.AIO.AioGetAiSamplingCount()
            AiData, _AiSamplingTimes = self.AIO.AioGetAiSamplingDataEx(self.AiSamplingCount)
            self.cnt += _AiSamplingTimes
            for i in range(self.AIO.AiChannels):
                npAiData = np.array(AiData)
                self.V[i] = np.append(self.V[i], npAiData[i:_AiSamplingTimes*self.AIO.AiChannels:self.AIO.AiChannels])
            # ----------------------------------------
            # デバイスの終了
            # ----------------------------------------
            V = np.array(self.V).T
            V = np.vstack([[i for i in range(1, self.AIO.AiChannels+1)], V])
            np.savetxt('./np_savetxt.csv', V, delimiter=',', fmt='%f')

            # ----------------------------------------
            # デバイスの終了
            # ----------------------------------------
            self.AIO.AioStopAi()
            self.AIO.AioExit()
            sys.exit()
        except KeyboardInterrupt:
            self.AiSamplingCount = self.AIO.AioGetAiSamplingCount()
            AiData, _AiSamplingTimes = self.AIO.AioGetAiSamplingDataEx(self.AiSamplingCount)
            self.cnt += _AiSamplingTimes
            for i in range(self.AIO.AiChannels):
                npAiData = np.array(AiData)
                self.V[i] = np.append(self.V[i], npAiData[i:_AiSamplingTimes*self.AIO.AiChannels:self.AIO.AiChannels])
            V = np.array(self.V).T
            V = np.vstack([[i for i in range(1, self.AIO.AiChannels+1)], V])
            np.savetxt('./np_savetxt.csv', V, delimiter=',', fmt='%f')
            # ----------------------------------------
            # デバイスの終了
            # ----------------------------------------
            self.AIO.AioStopAi()
            self.AIO.AioExit()
            sys.exit()

    def update(self):
        while self.win.isVisible():
            self.AiSamplingCount = self.AIO.AioGetAiSamplingCount()
            # print(self.AiSamplingCount)
            if self.AiSamplingCount >= self.AIO.MaxAiSamplingTimes//10:
                # self.AiSamplingCount -= self.AIO.AiSamplingTimes
                AiData, _AiSamplingTimes = self.AIO.AioGetAiSamplingDataEx(self.AiSamplingCount)
                print(_AiSamplingTimes)
                self.cnt += _AiSamplingTimes
                # print("!!!!!!!!!!")

                for i in range(self.AIO.AiChannels):
                    npAiData = np.array(AiData)
                    self.V[i] = np.append(self.V[i], npAiData[i:_AiSamplingTimes*self.AIO.AiChannels:self.AIO.AiChannels])
                    self.curves[i].setData(self.V[i][max(0, self.cnt - self.TIMERANGE):])
                    # curves[i].setData(self.V[i])
                # print(len(self.V[0]))
                self.frg = True
                
                # ptr += 1
            pass

    def fft(self):
        while self.win.isVisible():
            try:
                
                # print(11111111111111)
                np.fft.fft(self.V[0][0:1024])
                pass
            except:
                pass
        #     print("-", end='')
        pass


if __name__ == '__main__':
    m = main()
