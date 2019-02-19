import unicodedata

from funcy import compose
from lxml import html
from lxml.html.clean import clean_html
from polyglot.tokenize import WordTokenizer
from polyglot.base import Sequence
import Stemmer


class Preprocess:
    def __init__(self, lang, use_stemmer, stop_words):
        self.lang = lang
        self.use_stemmer = use_stemmer
        self.word_tokenizer = WordTokenizer(locale=lang)
        # As we have only one language currently, no need to
        # check if supported
        self.stemmer = Stemmer.Stemmer(self.lang)
        self.stop_words = stop_words

    def stem(self, tokens):
        return (self.stemmer.stemWords(tokens)
                if self.use_stemmer
                else tokens)

    def remove_accents(self, text):
        return (unicodedata.normalize('NFD', text)
                .encode('ascii', 'ignore')
                .decode("utf-8"))

    def lower(self, text):
        return text.lower()

    def clear_html(self, text):
        # Html cleaner will throw exception when an incorrect tag
        # formation is detected a 'prompt' like symbol e.g.: '<- '
        try:
            text = clean_html(html.fromstring(text)).text_content()
        except Exception as e:
            pass
        return text

    def is_token_stopword(self, token):
        return token in self.stop_words

    def is_alpha(self, token):
        return token.isalpha()

    def filtertokens(self, tokens):
        return filter(
            lambda t: self.is_alpha(t) and not (self.is_token_stopword(t)),
            tokens)

    def transform2words(self, text):
        return self.word_tokenizer.transform(Sequence(text)).tokens()

    def process(self, text):
        fnlist = [
            self.remove_accents,
            self.lower,
            self.clear_html,
            self.transform2words,
            self.filtertokens,
            self.stem
        ]
        return compose(*reversed(fnlist))(text)
