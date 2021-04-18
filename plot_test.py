import sys
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg
import numpy as np
 
app = QApplication(sys.argv)
 
 
x = np.random.normal(size=1000)
y = np.random.normal(size=1000)
p1 = pg.plot(x, y, pen=None, symbol='o')

p1.setXRange(5, 20, padding=0)

status = app.exec_()
sys.exit(status)