import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QWidget,\
    QToolBar
from text_processor import TextProcessor, KeywordSelectionDialog


class TextEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Text Editor')
        self.setGeometry(100, 100, 600, 400)

        # Create a central widget and set the layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Create a QTextEdit to display the text
        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        # Create a button 
        open_button = QPushButton('Open Text File', self)
        open_button.clicked.connect(self.open_file)
        layout.addWidget(open_button)

        key_word_button = QPushButton('Keyword Extraction', self)
        key_word_button.clicked.connect(self.key_word_extract)
        layout.addWidget(key_word_button)

        central_widget.setLayout(layout)

        # Create a menu bar
        menubar = self.menuBar()

        # Add a "File" menu
        file_menu = menubar.addMenu('File')

        # Add actions to the "File" menu
        open_action = file_menu.addAction('Open', self.open_file)

        #Create a toolbar
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)

        #Add actions
        open_action = toolbar.addAction('Open', self.open_file)
        toolbar.addSeparator()  # Add a separator between actions

    def open_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Text Files (*.txt);;XML Files (*.xml);;Ebook Files (*.epub *.pdf);;PDF Files (*.pdf);;All Files (*)")

        file_name, _ = file_dialog.getOpenFileName(self, "Open File", "", "All Files (*)")

        if file_name:
            with open(file_name, 'r') as file:
                text = file.read()
                self.text_edit.setPlainText(text)

    def key_word_extract(self):
        #Create instance
        text_processor = TextProcessor()
        text_processor.key_word_extraction()




        
               




def main():
    app = QApplication(sys.argv)
    window = TextEditorApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
