import os
import sys 
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, \
QToolBar, QVBoxLayout, QTextEdit, QFileDialog
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

        #Clean HTML and XML
        clean_file_action = QAction(QIcon("icons/clean.png"), "Clean HTML/XML", self)
        clean_file_action.triggered.connect(self.clean_file)
        file_menu_item.addAction(clean_file_action)

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

        #Central Widget
        self.central_widget.setLayout(self.layout)

    def upload(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Text Files (*.txt);;XML Files (*.xml);;Ebook Files (*.epub *.pdf);;PDF Files (*.pdf);;All Files (*)")
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "All Files (*)")

        #Read File Content when selected and put it in original_text_edit
        if file_path:
            with open(file_path, encoding="utf8") as file: 
                file_contents = file.read()
                self.original_text_edit.setPlainText(file_contents)
                return file_path

    def clean_file(self):
        if not hasattr(self, 'file_path'):
            self.upload()  # If file_path attribute is not set, trigger file upload

        if not self.file_path:
            return

        file_extension = os.path.splitext(self.file_path)[1].lower()

        if file_extension == '.xml':
            cleaned_text = self.clean_xml_file(self.file_path)
        elif file_extension in ['.html', '.htm']:
            cleaned_text = self.clean_html_file(self.file_path)
        else:
            self.keywords_text_edit.setPlainText("Unsupported file format.")
            return

        self.original_text_edit.setPlainText(cleaned_text)

    def clean_html_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        cleaned_text = soup.get_text(separator='\n', strip=True)
        return cleaned_text

    def clean_xml_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            xml_content = file.read()

        root = ET.fromstring(xml_content)
        cleaned_text = ' '.join(root.itertext())
        return cleaned_text

    def extract_keywords(self):
        text = self.original_text_edit.toPlainText()
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
