import bs4


class Word:
    def __init__(self, word_raw_data: bs4.element.Tag):
        self._raw_data = word_raw_data
        self._word = word_raw_data.next

    def __repr__(self):
        return self._word

    @property
    def raw_data(self):
        return self._raw_data


    def is_binyan_hifil(self):
        mini_words = self._raw_data.find_all("m")
        is_hifil = False
        for m in mini_words:
            if "HIFIL" in m.get("ana", ""):
                is_hifil = True
                break
        return is_hifil
