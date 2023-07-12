import bs4
from BibleSentence import BibleSentence


class Chapter:
    def __init__(self, raw_data: bs4.element.Tag):
        self._raw_data = raw_data
        self._id: str = raw_data.get("xml:id", "Get Error")
        self._sentences: list('Sentence') = [BibleSentence(raw_sentence_data) for raw_sentence_data in raw_data.find_all("s")]

    @property
    def raw_data(self):
        return self._raw_data

    @property
    def chapter_id(self):
        return self._id

    @property
    def sentences(self):
        return self._sentences

    def get_sentences_with_hifeil(self) -> list('Sentence'):
        return [s for s in self._sentences if s.has_binyan_hifil()]

    def __repr__(self):
        clean_chapter = ""
        for sentence in self._sentences:
            clean_chapter += str(sentence) + ":\n"
        return clean_chapter

    @property
    def id(self):
        return self._id
