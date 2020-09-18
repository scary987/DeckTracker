import sys;
from PyQt5 import QtGui, QtCore,QtWidgets;
from PyQt5.QtWidgets import QMainWindow , QLabel, QWidget, QPushButton;
from PyQt5.QtGui import QPainter,QPen, QColor;
from PyQt5.QtCore import Qt,QSize;


class DeckGUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(600,200))
        self.setWindowTitle("Scary DeckTracker GUI")

        
        b2 = QPushButton('Button 2 ',self)
        b2.move(50,50)
        b2.resize(b2.sizeHint())
        b2.clicked.connect(self.clicked2)

    def clicked2(self):
        print('Button 2 wurde angeklickt. Programmende')
        app.quit()

app= QtWidgets.QApplication([])
win=DeckGUI()
win.show()
app.exec_()