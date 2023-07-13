from BGU_CS_NLP_Project.sentence_vector_creation.word import Word, find_gender, find_number, find_tense, find_word_type, find_person
from typing import List
import json
import pandas as pd


class Sentence:
    def __init__(self, source: str, id: str, hifeil_index: int, _words: List[Word],
                 rosen_def: int = -1, glirt_def: int = -1):
        self._source = source
        self._id = id
        self._len = len(_words)
        self._hifeil_index = hifeil_index
        self._rosen_def = rosen_def
        self._glirt_def = glirt_def
        self._words = _words

    def to_dict(self):
        dictionary = {'source': self._source,
                'id': self._id,
                'len': self._len,
                'hifeil_index': self._hifeil_index,
                'rosen_definition': self._rosen_def,
                'glirt_definition': self._glirt_def}
        count = 1
        for word in self._words:
            word_number = "word" + str(count)
            dictionary[word_number] = word.__dict__
            count = count + 1
        return dictionary

    @staticmethod
    def convert_sentences_to_json(sentences: List['Sentence'], name="sentences_bible.json"):
        serialized_data = [sentence.to_dict() for sentence in sentences]
        with open(name, 'w', encoding='utf-8') as f:
            json.dump(serialized_data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def get_sentences_from_json(json_file_path: str) -> List['Sentence']:
        with open(json_file_path, encoding='utf-8') as fh:
            data = json.load(fh)
        sentences = []
        for item in data:
            source = item['source']
            id = item['id']
            hifeil_index = int(item['hifeil_index'])
            rosen_def = int(item['rosen_definition'])
            glirt_def = int(item['glirt_definition'])
            words = []
            count = 1
            while item.get(("word" + str(count)), None) is not None:
                word_json = item["word" + str(count)]
                gender = find_gender(word_json['_male'], word_json['_female'])
                number = find_number(word_json['_singular'], word_json['_plural'], word_json['_dual'])
                tense = find_tense(word_json['_tense_past'], word_json['_tense_present'], word_json['_tense_future'])
                word_type = find_word_type(word_json['_adp'], word_json['_propn'], word_json['_verb'], word_json['_adj'],
                                           word_json['_conj'], word_json['_noun'], word_json['_det'],
                                           word_json['_adv'], word_json['_aux'], word_json['_pron'])
                person = find_person(word_json['_first_person'], word_json['_second_person'],
                                     word_json['_third_person'], word_json['_any'])
                word = Word(word_json['_source'], word_json['_word'], gender, number, tense, word_type, person)
                words.append(word)
                count = count + 1
            sentence = Sentence(source, id, hifeil_index, words, rosen_def, glirt_def)
            sentences.append(sentence)
        return sentences

    def _sentence_vector_dict(self, words_prev, words_after) -> dict:
        word_properties = self._words[0].properties_dict().keys()
        vector_dict = {"id": self._id, "source": self._source, "len": self._len, "glirt_def": self._glirt_def, "rosen_def": self._rosen_def}
        hifeil_properties = self._words[self._hifeil_index].properties_dict()
        for property in word_properties:
            vector_dict["hifeil_" + property] = hifeil_properties[property]

        # add propeties of {words_prev} words before hifeil verb
        for i in range(1, words_prev+1):
            word_idx = self._hifeil_index - i
            if word_idx < 0:
                vector_dict.update({"prev_word_" + str(i) + "_" + p: 0 for p in word_properties})
            else:
                vector_dict.update({"prev_word_" + str(i) + "_" + p: v for p, v in self._words[word_idx].properties_dict().items()})

        # add propeties of {words_after} words after hifeil verb
        for i in range(1, words_after+1):
            word_idx = self._hifeil_index + i
            if word_idx > self._len-1:
                vector_dict.update({"after_word_" + str(i) + "_" + p: 0 for p in word_properties})
            else:
                vector_dict.update({"after_word_" + str(i) + "_" + p: v for p, v in self._words[word_idx].properties_dict().items()})
        return vector_dict


    @staticmethod
    def create_sentence_vector(sentences: List['Sentence'], words_prev: int = 2, words_after: int = 2) -> pd.DataFrame:
        rows = [s._sentence_vector_dict(words_prev, words_after) for s in sentences]
        for r in rows:
            del r["hifeil_properties_dict"]
            for i in range(1, words_prev + 1):
                del r["prev_word_" + str(i) + "_" + "properties_dict"]
            for i in range(1, words_after + 1):
                del r["after_word_" + str(i) + "_" + "properties_dict"]

        return pd.DataFrame(rows, columns=rows[0].keys())


if __name__ == "__main__":
    sentences = Sentence.get_sentences_from_json("json_files/tagged_sentences_data.json")
    df = Sentence.create_sentence_vector(sentences, 4, 0)
    print(df.head(10))