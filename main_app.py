import sys 
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, \
QToolBar, QVBoxLayout, QTextEdit, QFileDialog
from PyQt6.QtGui import QAction, QIcon
import spacy

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Spacy Text Processor")
        self.setMinimumSize(800, 800)

        #Menu Bar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        search_menu_item = self.menuBar().addMenu("&Search")

        #Add ACtions to menuBar
        upload_file_action = QAction(QIcon("icons/upload_file.png"), "Upload File", self)
        upload_file_action.triggered.connect(self.upload)
        file_menu_item.addAction(upload_file_action)

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
