import bs4
from BibleWord import BibleWord


class BibleSentence:
    def __init__(self, raw_data: bs4.element.Tag):
        self._id = raw_data.get("xml:id", "Got Error")
        self._raw_data = raw_data
        self._words = [BibleWord(word_raw_data) for word_raw_data in raw_data.find_all("w")]
        self._hifil_word = None

    @property
    def id(self):
        return self._id

    @property
    def raw_data(self):
        return str(self._raw_data).replace("\n", " ")

    @property
    def words(self):
        return self._words

    @property
    def hifil_word(self) -> BibleWord:
        return self._hifil_word

    def __repr__(self):
        clean_sentence = ""
        for word in self._words:
            clean_sentence += str(word)+" "
        return clean_sentence.strip()

    def has_binyan_hifil(self) -> bool:
        has_hifil = False
        for word in self._words:
            if word.is_binyan_hifil():
                has_hifil = True
                self._hifil_word = word
                break
        return has_hifil