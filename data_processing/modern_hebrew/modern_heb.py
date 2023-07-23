import pandas as pd
from sentence import Sentence
from word import Word, Gender, Number, Tense, WordType, Person

SOURCE = "modernHebrew"


def word_gender(words):
    if "Gender=Fem" in words[5]:
        return Gender.FEMALE
    elif "Gender=Masc" in words[5]:
        return Gender.MALE
    elif "Gender=" in words[5]:
        print("gender not found\n" + str(words))
        return Gender.NONE
    return Gender.NONE


def word_number(words):
    if "Number=Sing" in words[5]:
        return Number.SINGULAR
    elif "Number=Plur" in words[5]:
        return Number.PLURAL
    elif "Number=Dual" in words[5]:
        return Number.DUAL
    elif "Number=" in words[5]:
        print("number not found\n" + str(words))
        return Number.NONE
    else:
        return Number.NONE


def word_tense(words):
    if "Past" in words[5]:
        return Tense.PAST
    elif "Pres" in words[5]:
        return Tense.PRESENT
    elif "Fut" in words[5]:
        return Tense.FUTURE
    elif "Tense" in words[5]:
        print("tense not found in:\n"+str(words))
        return Tense.NONE
    else:
        return Tense.NONE


def word_wordtype(words):
    if "Foreign=Yes" in words[5]:
        return WordType.NOUN
    if "ADP" in words[3]:
        return WordType.ADP
    elif "VERB" in words[3] or "VerbType=" in words[5] or "HebBinyan=" in words[5]:
        return WordType.VERB
    elif "AUX" in words[3]:
        return WordType.AUX
    elif "DET" in words[3]:
        return WordType.DET
    elif "ADV" in words[3]:
        return WordType.ADV
    elif "PROPN" in words[3]:
        return WordType.PROPN
    elif "PRON" in words[3]:
        return WordType.PRON
    elif "ADJ" in words[3]:
        return WordType.ADJ
    elif "CONJ" in words[3] or "SCONJ" in words[3] or "CCONJ" in words[3]:
        return WordType.CONJ
    elif "NUM" in words[3]:
        return WordType.NOUN
    elif "NOUN" in words[3] or "Foreign=Yes" in words[5]:
        return WordType.NOUN
    else: #defualt value for foreign untagged words
        return WordType.NOUN


def word_person(words):
    if "Person=1" in words[5]:
        return Person.FIRST
    elif "Person=2" in words[5]:
        return Person.SECOND
    elif "Person=3" in words[5]:
        return Person.THIRD
    elif "Person" in words[5]:
        print("person not found in:\n"+str(words))
        return Person.NONE
    else:
        return Person.NONE


def word_builder(words):
    word_data = {}
    word_data["WordType"] = word_wordtype(words)
    word_data["Gender"] = word_gender(words)
    word_data["Number"] = word_number(words)
    word_data["Tense"] = word_tense(words)
    word_data["Person"] = word_person(words)
    return Word(SOURCE, words[1], word_data["Gender"], word_data["Number"], word_data["Tense"], word_data["WordType"], word_data["Person"])


def data_parser():
    paths = ['modern_hebrew_data/he_iahltwiki-ud-train.conllu.txt']
    sentences_per_path = []
    for path in paths:
        sentences = single_file_data_parser(path)
        sentences_per_path.append(sentences)
    return [sentence for path_sentences in sentences_per_path for sentence in path_sentences]


def single_file_data_parser(file_name):
    count = 0
    sentences = []
    with open(file_name, encoding='utf-8') as file:
        while True:
            line = file.readline()
            count += 1
            if not line:
                break
            if line[2:9] == "sent_id":
                sent_id = line[12:line.__len__()-1]
                file.readline() # skip first text = line
                words_of_sentence = []
                line = file.readline()
                if not line or line is None:
                    break
                hifeil_index = -1
                while len(line) > 0 and line[0] != "#": # process a sentence
                    words = line.split()
                    if "-" not in words[0] and "PUNCT" not in words[3] and "SYM" not in words[3]:
                        word_object = word_builder(words)
                        words_of_sentence.append(word_object)
                        for index, word in enumerate(words): # iterate over word components
                            if "HebBinyan=HIFIL" in word and hifeil_index == -1:
                                hifeil_index = len(words_of_sentence)-1
                    # once hifeil is found, add Sentence, words will be updated
                    if hifeil_index != -1:
                        sentences.append(Sentence(SOURCE, sent_id, hifeil_index, words_of_sentence))
                    line = file.readline()
                    # print("line:"+line)
                    if line == '\n':
                        break
        return sentences


if __name__ == '__main__':
    sentence = data_parser()
    sentences_json = Sentence.convert_sentences_to_json(sentence, "sentences_modern_hebrew.json")