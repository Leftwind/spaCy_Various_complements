import spacy

class TextProcessor:
    def __init__(self):
        #load English model
        self.nlp = spacy.load("en_core_web_sm")

    def key_word_extraction(self, text, type):
        doc = self.nlp(text)

        # Extract keywords    
        keywords = [token.text for token in doc if token.pos_ == f"{type}"]

        return keywords