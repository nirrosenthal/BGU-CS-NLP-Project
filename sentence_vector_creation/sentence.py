from BGU_CS_NLP_Project.sentence_vector_creation.word import Word, find_gender, find_number, find_tense, find_word_type, find_person
from typing import List
import json


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


def get_joined_json_data():
    heb_sents = Sentence.get_sentences_from_json("../data_processing/modern_hebrew/sentences_modern_hebrew.json")
    bible_sents = Sentence.get_sentences_from_json("../data_processing/bible/sentences_bible.json")
    joined_sents = heb_sents + bible_sents
    Sentence.convert_sentences_to_json(joined_sents, "joined_sentences_no_tags.json")


def add_tagging_data():
    sentences = Sentence.get_sentences_from_json("json_files/joined_sentences_no_tags.json")
    tagged_sentences = []
    tagging_data_path = "json_files/bible_tags.json"
    with open(tagging_data_path, encoding='utf-8') as td:
        data = json.load(td)

    for sent in sentences:
        if data.get(sent._id, None) is not None:
            sent._rosen_def = data[sent._id]["rosen_def"]
            sent._glirt_def = data[sent._id]["glirt_def"]
            tagged_sentences.append(sent)

    Sentence.convert_sentences_to_json(tagged_sentences, "json_files/tagged_sentences_data.json")


if __name__== "__main__":
