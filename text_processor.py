from PyQt6.QtCore import Qt
import spacy
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QWidget


class KeywordSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        #DropDown Menu in the file: 
        self.keyword_type_combo = QComboBox()
        #Test Options
        self.keyword_type_combo.addItem("Nouns")
        self.keyword_type_combo.addItem("Verbs")

        #Load layout
        layout.addWidget(self.keyword_type_combo)

        #Confirm
        button_confirm = QPushButton("Extract Keywords")
        button_confirm.clicked.connect(self.accept)

        layout.addWidget(button_confirm)

        self.setLayout(layout)
        
    def get_selected_keyword_type(self):
        # Return the selected keyword type
        return self.keyword_type_combo.currentText()




class TextProcessor():
    def __init__(self):
        # Load the SpaCy English model
        self.nlp = spacy.load("en_core_web_sm")

    def accept(self, text, keyword_type="NOUN"):
        # Process the text using SpaCy
        doc = self.nlp(text)

        # Extract keywords based on the selected type
        if keyword_type == "NOUN":
            keywords = [token.text for token in doc if token.pos_ == "NOUN"]
        elif keyword_type == "VERB":
            keywords = [token.text for token in doc if token.pos_ == "VERB"]
        # Add more conditions for other keyword types as needed

        return keywords