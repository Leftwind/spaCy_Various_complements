import sys 
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, \
QToolBar, QVBoxLayout, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Spacy Text Processor")
        self.setMinimumSize(800, 800)

        #Create Central Widget: 
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        search_menu_item = self.menuBar().addMenu("&Search")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.original_text_edit = QTextEdit()
        self.layout.addWidget(self.original_text_edit)

        self.extract_button = QPushButton("Extract Keywords")
        self.extract_button.clicked.connect(self.extract_keywords)
        self.layout.addWidget(self.extract_button)

        self.keywords_text_edit = QTextEdit()
        self.keywords_text_edit.setReadOnly(True)  # Make it read-only
        self.layout.addWidget(self.keywords_text_edit)

        self.central_widget.setLayout(self.layout)

    def extract_keywords():
        pass    









def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
