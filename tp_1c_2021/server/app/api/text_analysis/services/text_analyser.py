import string
from typing import Dict, List, Tuple

import en_core_web_md
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer

from app.api.text_analysis.models import TextAnalysis
from app.api.text_analysis.services.spacy_text_analyser import SpacyTextAnalyser
from app.api.text_analysis.utils.text_utils import de_emojify, get_sentiment
from config import Config

"""
Source:
https://realpython.com/python-nltk-sentiment-analysis/
https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
NLTK doc
estudiar caso -> I'm not selling my BTC 
"""


class TextAnalyser:

    def __init__(self):
        self._analyser = SentimentIntensityAnalyzer()
        self.top_X_frequency = Config.X_FREQUENCY
        self.nlp = en_core_web_md.load()
        self.whitelisted_chars = ["$", "'", "#"]
        self.blacklisted_chars = ["√"]
        self.vectorizer = TfidfVectorizer()

    def _process_text(self, text) -> str:
        translation = str.maketrans('', '', "".join([c for c in string.punctuation if c not in self.whitelisted_chars]))
        delete_dict = {sp_character: '' for sp_character in self.blacklisted_chars}
        table = str.maketrans(delete_dict)
        return de_emojify(text).translate(translation).translate(table)

    def _get_frequency(self, text: str) -> Dict[str, List[str]]:
        lower_text = text.lower()
        tokens = nltk.word_tokenize(lower_text)
        freq = nltk.FreqDist(tokens)
        d = {}
        for key, value in freq.items():
            d.setdefault(value, []).append(key)
        return {str(k): d[k] for k in sorted(d.keys(), reverse=True)[:self.top_X_frequency]}

    def _get_ner(self, text: str) -> List[Tuple[str, str]]:
        doc = self.nlp(text)
        return [(X.text, X.label_) for X in doc.ents]

    def analyse(self, text) -> TextAnalysis:
        processed_text = self._process_text(text)
        polarity = self._analyser.polarity_scores(processed_text)
        compound_value = polarity["compound"]

        return TextAnalysis(
            original_text=text,
            processed_text=processed_text,
            sentiment=get_sentiment(compound_value),
            frequency=self._get_frequency(processed_text),
            ner=self._get_ner(processed_text),
            tokenized=nltk.word_tokenize(processed_text)
        )


# text_analyser = TextAnalyser()
text_analyser = SpacyTextAnalyser()
