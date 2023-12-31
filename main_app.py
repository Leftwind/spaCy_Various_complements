import sys 
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, \
QVBoxLayout, QTextEdit, QFileDialog, QMessageBox, QDialog, QComboBox
from PyQt6.QtGui import QAction, QIcon
import spacy
from bs4 import BeautifulSoup
from spacy.matcher import Matcher


#Global Variables:
class DefaultSettings:
    #NLP Extract
    nlp = spacy.load("en_core_web_sm")

    @classmethod
    def change_nlp(cls, new_value):
        cls.nlp = new_value

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
        config_menu_item = self.menuBar().addMenu("&Config")
        search_menu_item = self.menuBar().addMenu("&Search")

        #Add ACtions to menuBar
        upload_file_action = QAction(QIcon("icons/upload_file.png"), "Import File", self)
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

        #Select NLP
        select_nlp_action = QAction(QIcon("icons/procesamiento-natural-del-lenguaje.png"), "Change NLP Load", self)
        select_nlp_action.triggered.connect(self.select_nlp)
        config_menu_item.addAction(select_nlp_action)

        #NEP
        nep_action = QAction(QIcon("icons/job.png"), "Name Entity Recog", self)
        nep_action.triggered.connect(self.nep)
        file_menu_item.addAction(nep_action)

        #Matcher
        matcher_action = QAction(QIcon("icons/puzzle.png"), "Custom Matcher", self)
        matcher_action.triggered.connect(self.match)
        file_menu_item.addAction(matcher_action)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

        self.extract_button = QPushButton("Extract Keywords")
        self.extract_button.clicked.connect(self.extract_keywords)
        self.layout.addWidget(self.extract_button)

        self.nep_button = QPushButton("NEP")
        self.nep_button.clicked.connect(self.nep)
        self.layout.addWidget(self.nep_button)

        self.match_button = QPushButton("Custom Matcher")
        self.match_button.clicked.connect(self.match)
        self.layout.addWidget(self.match_button)

        #Central Widget
        self.layout.addStretch()
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
        content = self.text_edit.toPlainText()
        #Funciona peor
        #CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        #cleantext = re.sub(CLEANR, '', content)      

        #There is also the option of using BS4: Funciona mucho mejor, porque elimina los espacios
        
        cleantext = BeautifulSoup(content, "lxml").text
        self.text_edit.setPlainText(cleantext)

    def extract_keywords(self):
        extract_keywords = KeywordWindow(self)
        extract_keywords.exec()

    def select_nlp(self):
        select_nlp = NlpLoadSelect()
        select_nlp.exec()

    def nep(self):
        nep = NameEntityRecog(self)
        nep.exec()

    def match(self):
        matche = CustomMathcer(self)
        matche.exec()


class NlpLoadSelect(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select spacy load")
        self.setWindowIcon(QIcon("icons/logo.png"))
        self.setMinimumSize(200, 100)

        self.accept_button = QPushButton("Change Load", self)
        
        #Combo_box Items
        self.combo_box = QComboBox(self)
        self.combo_box.addItem("English")
        self.combo_box.addItem("Spanish")
        self.combo_box.addItem("German")

        #Layout
        layout = QVBoxLayout()
        layout.addWidget(self.accept_button)
        layout.addWidget(self.combo_box)

        #Connectioon
        self.accept_button.clicked.connect(self.change_nlp)
        
        #Set up
        self.setLayout(layout)

    def change_nlp(self):
        selected_language = self.combo_box.currentText()

        if selected_language == "English":
            DefaultSettings.change_nlp(spacy.load("en_core_web_sm"))
        elif selected_language == "Spanish":
            DefaultSettings.change_nlp(spacy.load("es_core_news_sm"))   
        elif selected_language == "German":
            DefaultSettings.change_nlp(spacy.load("de_core_news_sm")) 

        self.accept()    

class KeywordWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        self.setWindowTitle("Extracted Keywords")
        self.setWindowIcon(QIcon("icons/logo.png"))
        self.setMinimumSize(400, 400)

        layout = QVBoxLayout()

        self.keywords_text_edit = QTextEdit()
        self.keywords_text_edit.setReadOnly(True)  # Make it read-only
        layout.addWidget(self.keywords_text_edit)

        # Set the layout on the main widget
        self.setLayout(layout)

        self.keyword_extract()

    def keyword_extract(self):
        text = self.main_window.text_edit.toPlainText()
        
        doc = DefaultSettings.nlp(text)
        keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
        self.keywords_text_edit.setPlainText(', '.join(keywords))       

class NameEntityRecog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        self.setWindowTitle("NER")
        self.setWindowIcon(QIcon("icons/logo.png"))
        self.setMinimumSize(400, 400)
        
        layout = QVBoxLayout()

        self.keywords_text_edit = QTextEdit()
        self.keywords_text_edit.setReadOnly(True)  # Make it read-only
        layout.addWidget(self.keywords_text_edit)

        # Set the layout on the main widget
        self.setLayout(layout)

        self.name_entity_recog()

    def name_entity_recog(self):
        text = self.main_window.text_edit.toPlainText()

        doc = DefaultSettings.nlp(text )
        entities_text = ""

        for ent in doc.ents:
            entities_text += f"{ent.text} ({ent.label_})\n"

        self.keywords_text_edit.setPlainText(entities_text)    

class CustomMathcer(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Custom Matcher")
        self.setWindowIcon(QIcon("incons/logo.png"))
        self.setMinimumSize(400,400)

        layout = QVBoxLayout()

        #Need to create different options to create the line of code. 
        #Need to modify this: pattern = [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}]
        self.first_argument_combo = QComboBox()
        self.second_argument_combo = QComboBox()
        self.third_argument_combo = QComboBox()

        #Add items
        #self.first_argument_combo.addItem() 
         
        #Need a patter name: 

        #We will create 3 differente comboBoxes that will be printed in a small Qdialog Window, that can be managed by hand
        #Then it will be send too the matcher:
        #pattern_created = Sum of all of the things, also QDialog.

        def matcher(self):
            matcher = Matcher(DefaultSettings.nlp.vocab)

            #Add Pattern
            pattern = self.pattern_created
            matcher.add("HelloWorld", [pattern])

            doc = DefaultSettings.nlp("Hello, world! Hello world!")
            matches = matcher(doc)
            for match_id, start, end in matches:
                string_id = DefaultSettings.nlp.vocab.strings[match_id]  # Get string representation
                span = doc[start:end]  # The matched span
                print(match_id, string_id, start, end, span.text)
        


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
