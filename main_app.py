import os
import sys 
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, \
QToolBar, QVBoxLayout, QTextEdit, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import spacy
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Spacy Text Processor")
        self.setWindowIcon(QIcon("icons/logo.png"))
        self.setMinimumSize(800, 800)

        #Menu Bar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        search_menu_item = self.menuBar().addMenu("&Search")

        #Add ACtions to menuBar
        upload_file_action = QAction(QIcon("icons/upload_file.png"), "Upload File", self)
        upload_file_action.triggered.connect(self.upload)
        file_menu_item.addAction(upload_file_action)

        #Save
        save_as_action = QAction(QIcon("icons/diskette.png"), "Save as", self)
        save_as_action.triggered.connect(self.save_as)
        file_menu_item.addAction(save_as_action)

        #Clean HTML and XML
        clean_file_action = QAction(QIcon("icons/clean.png"), "Clean HTML/XML", self)
        clean_file_action.triggered.connect(self.clean_file)
        file_menu_item.addAction(clean_file_action)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

        self.extract_button = QPushButton("Extract Keywords")
        self.extract_button.clicked.connect(self.extract_keywords)
        self.layout.addWidget(self.extract_button)

        self.keywords_text_edit = QTextEdit()
        self.keywords_text_edit.setReadOnly(True)  # Make it read-only
        self.layout.addWidget(self.keywords_text_edit)

        #Central Widget
        self.central_widget.setLayout(self.layout)

    def upload(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Text Files (*.txt);;XML Files (*.xml);;Ebook Files (*.epub *.pdf);;PDF Files (*.pdf);;All Files (*)")
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "All Files (*)")

        #Read File Content when selected and put it in text_edit
        if file_path:
            with open(file_path, encoding="utf8") as file: 
                file_contents = file.read()
                self.text_edit.setPlainText(file_contents)
                return file_path

    def save_as(self):
        dialog = QFileDialog()
        dialog.setOptions(QFileDialog.Option.DontUseNativeDialog)
        file_name, _ = dialog.getSaveFileName(self, "Save As", "", "Text Files (*.txt);;All Files (*)")

        if file_name:
            content = self.text_edit.toPlainText()
            try:
                with open(file_name, 'w') as file:
                    file.write(content)
                QMessageBox.information(self, 'Success', f'Successfully saved in {file_name}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error: {e}')


    def clean_file(self):
        pass

    def extract_keywords(self):
        text = self.text_edit.toPlainText()
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
        self.keywords_text_edit.setPlainText(', '.join(keywords))











def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
