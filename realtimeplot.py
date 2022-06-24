import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from time import time

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


app = pg.mkQApp("Plotting Example")
# mw = QtWidgets.QMainWindow()
# mw.resize(800,800)

win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
win.resize(1000, 600)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

p6 = win.addPlot(title="Updating plot")
curve = p6.plot(pen='b')
data = np.random.normal(size=(10, 1000))
ptr = 0
data = np.zeros([100])
data = np.sin
x = np.linspace(0, 5*np.pi, 5000)
y = np.sin(x)
old = time()
now = time()


def update():
    global curve, data, ptr, p6, now, old
    now = time()
    curve.setData(np.sin(x+ptr*0.1))
    if ptr == 0:
        p6.enableAutoRange('xy', False)  # stop auto-scaling after the first data set is plotted
    ptr += 1
    if ptr % 10 == 0:
        p6.setTitle((now-old)*1000)
    old = now


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(10)


if __name__ == '__main__':
    pg.exec()
