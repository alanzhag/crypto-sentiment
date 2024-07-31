import re
import string
from typing import Dict, List, Tuple

import emoji
import en_core_web_md
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.en.stop_words import STOP_WORDS
from spacytextblob.spacytextblob import SpacyTextBlob

from app.api.text_analysis.models import TextAnalysis
from app.api.text_analysis.utils.text_utils import get_sentiment, emoticon_string
from config import Config

"""
Source:
https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da
https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
https://spacy.io/universe/project/spacy-textblob
https://stackoverflow.com/questions/62141647/remove-emojis-and-users-from-a-list-in-python-and-punctuation-nlp-problem-and
https://www.dataquest.io/blog/tutorial-text-classification-in-python-using-spacy/
NLTK doc
estudiar caso -> I'm not selling my BTC 
"""


class SpacyTextAnalyser:

    def __init__(self):
        SpacyTextBlob
        self.top_X_frequency = Config.X_FREQUENCY
        self.nlp = en_core_web_md.load()
        self.nlp.add_pipe('spacytextblob')
        self.whitelisted_chars = ["$", "'", "#"]
        self.blacklisted_chars = ["√"]
        self.vectorizer = TfidfVectorizer()
        self.stop_words = spacy.lang.en.stop_words.STOP_WORDS
        self.punctuations = string.punctuation

    def give_emoji_free_text(self, text):
        return emoji.get_emoji_regexp().sub(r'', text)

    def sanitize(self, string_to_sanitize):
        """ Sanitize one string """

        # remove graphical emoji
        sanitized_string = self.give_emoji_free_text(string_to_sanitize)

        # remove textual emoji
        sanitized_string = re.sub(emoticon_string, "", sanitized_string)

        # normalize to lowercase
        sanitized_string = sanitized_string.lower()

        # remove user
        # assuming user has @ in front
        sanitized_string = re.sub(r"""(?:@[\w_]+)""", "", sanitized_string)

        # remove urls
        sanitized_string = re.sub(r'(http|https)://[\w\-]+(\.[\w\-]+)+\S*', "", sanitized_string)

        # remove more aggresive urls
        sanitized_string = re.sub(r"www\.[a-zA-Z]+\.[a-zA-Z]+", "", sanitized_string)

        # remove # and @
        for punc in '":!@#':
            sanitized_string = sanitized_string.replace(punc, "")

        # remove ellipsis .. and ...
        sanitized_string = re.sub(r"[.]{2,3}", "", sanitized_string)

        # remove ||
        sanitized_string = re.sub(r"\|\|", "", sanitized_string)

        # remove 't.co/' links
        sanitized_string = re.sub(r'(http|https)//t.co\/[^\s]+', "", sanitized_string, flags=re.MULTILINE)

        return sanitized_string

    def __text_preprocessing(self, sentence):
        if sentence == "":
            return ""
        # Creating our token object, which is used to create documents with linguistic annotations.
        mytokens = self.nlp(sentence)

        # Lemmatizing each token and converting each token into lowercase
        mytokens = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens]

        # Removing stop words
        mytokens = [word for word in mytokens if word not in self.stop_words and word not in self.punctuations]

        # return preprocessed list of tokens
        return " ".join(mytokens)

    def _get_frequency_by_tf_idf(self, text: str) -> Dict[str, List[str]]:
        if not text:
            return {}
        vectors = self.vectorizer.fit_transform([text])
        feature_names = self.vectorizer.get_feature_names()
        dense = vectors.todense()
        dense_list = dense.tolist()
        d = {name: dense_list[0][index] for index, name in enumerate(feature_names)}
        return {str(k): d[k] for k in sorted(d.keys(), reverse=True)[:self.top_X_frequency]}

    def _get_ner(self, text) -> List[Tuple[str, str]]:
        doc = self.nlp(text)
        return [(X.text, X.label_) for X in doc.ents]

    def _tokenize(self, text) -> List[str]:
        doc = self.nlp(text)
        return [token for token in doc]

    def analyse(self, text) -> TextAnalysis:
        sanitized_text = self.sanitize(text)
        preprocessed_text = self.__text_preprocessing(sanitized_text)
        original_doc = self.nlp(text)

        return TextAnalysis(
            original_text=text,
            sanitized_text=sanitized_text,
            processed_text=preprocessed_text,
            sentiment=get_sentiment(original_doc._.polarity),
            polarity=original_doc._.polarity,
            subjectivity=original_doc._.subjectivity,
            frequency=self._get_frequency_by_tf_idf(preprocessed_text),
            ner=self._get_ner(preprocessed_text)
        )
