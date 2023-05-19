from word import Word
from typing import List


class Sentence:
    def __init__(self, source: str, id: str, hifeil_index: int, words: List[Word],
                 rosen_def: int = -1, glirt_def: int = -1):
        self._source = source
        self._id = id
        self._len = len(words)
        self._hifeil_index = hifeil_index
        self._rosen_def = rosen_def
        self._glirt_def = glirt_def
        self._words = words

    # TODO gal
    @staticmethod
    def convert_sentences_to_json(sentences: List['Sentence']):
        pass

    # TODO gal
    @staticmethod
    def get_sentences_from_json(json_file_path: str) -> List['Sentence']:
        return []
