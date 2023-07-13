from sentence import Sentence
import json


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
    sentences = Sentence.get_sentences_from_json("json_files/joined_sentences_no_tags.json")
    hm = [s for s in sentences if s._hifeil_index < 2]
    print(len(hm))