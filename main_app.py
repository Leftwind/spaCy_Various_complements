import sys 
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, \


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindwoTitle("Spacy Text Processor")
        self.setBaseSize()