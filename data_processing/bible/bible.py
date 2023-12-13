from source.Book import Book
from source.BibleSentence import BibleSentence
from typing import List
import pandas as pd
from BGU_CS_NLP_Project.sentence_vector_creation.sentence import Sentence
from BGU_CS_NLP_Project.sentence_vector_creation.word import Word, Gender, Number, Tense, WordType, Person

def get_filtered_bible_sentences_csv():
    sentences = Book.get_all_sentences_with_hifeil(["bible_data/Prophets.xml", "bible_data/Torah.xml", "bible_data/Writings.xml"])
    hifeil_word_col = [str(sen.hifil_word) for sen in sentences]
    pasuk_id_col = [sen.id for sen in sentences]
    pasuk_plain_text_col = [str(sen) for sen in sentences]
    pasuk_raw_data_col = [sen.raw_data for sen in sentences]
    df = pd.DataFrame({'sentence_id': pasuk_id_col,'hifil_word': hifeil_word_col,
                       'pasuk_text': pasuk_plain_text_col, 'xml_raw_data':pasuk_raw_data_col})
    df.to_csv("filtered_bible_sentences.csv", index=False, encoding="utf-8")


def convert_word(bible_word) -> Word:
    bible_word_str = str(bible_word)
    gender = (Gender.MALE if "GENDER_MASCULINE" in bible_word_str
              else (Gender.FEMALE if "GENDER_FEMININE" in bible_word_str else Gender.NONE))
    number = (Number.SINGULAR if "NUMBER_SINGULAR" in bible_word_str
              else (Number.PLURAL if "NUMBER_PLURAL" in bible_word_str
                    else (Number.DUAL if "NUMBER_DUAL" in bible_word_str else Number.NONE)))

    tense = (Tense.PAST if "TENSE_PAST" in bible_word_str else (
                Tense.PRESENT if "TENSE_TOINFINITIVE" in bible_word_str
                or "TENSE_IMPERATIVE" in bible_word_str
                or "TENSE_BAREINFINITIVE" in bible_word_str else (
                    Tense.FUTURE if "TENSE_FUTURE" in bible_word_str else Tense.NONE)))

    word_type = (WordType.ADP if "POS_ADPOSITION" in bible_word_str or "PREPOSITION" in bible_word_str else (
                WordType.PROPN if "POS_PROPERNAME" in bible_word_str else (
                    WordType.VERB if "POS_VERB" in bible_word_str or "BASEFORM_POS_PARTICIPLE" in bible_word_str else (
                    WordType.ADJ if "POS_ADJECTIVE" in bible_word_str else (
                    WordType.CONJ if "POS_CONJUNCTION" in bible_word_str or "PREFIX_FUNCTION_CONJUNCTION" in bible_word_str or "SUFFIX_FUNCTION_POSSESIVEPRONOUN" in bible_word_str else (
                    WordType.NOUN if "BASEFORM_POS_NOUN" in bible_word_str or "BASEFORM_POS_INITIALISM" in bible_word_str or "BASEFORM_POS_PARTICIPLE" in bible_word_str else (
                    WordType.ADV if "BASEFORM_POS_ADVERB" in bible_word_str or "BASEFORM_POS_NEGATION" in bible_word_str or "BASEFORM_POS_INTERJECTION" in bible_word_str or "INTERROGATIVE" in bible_word_str else (
                    WordType.DET if "PREFIX_FUNCTION_DEFINITEARTICLE" in bible_word_str else WordType.PRON
                    )
                    )))))))

    person = (Person.FIRST if "BASEFORM_PERSON_1" in bible_word_str else (
                Person.SECOND if "BASEFORM_PERSON_2" in bible_word_str else (
                    Person.THIRD if "BASEFORM_PERSON_3" in bible_word_str else (
                        Person.ANY if "BASEFORM_PERSON_ANY" in bible_word_str else Person.NONE))))

    return Word("Bible", str(bible_word.next), gender, number, tense, word_type, person)


def convert_sentence(sent: BibleSentence) -> Sentence:
    count = 0
    for word in sent.words:
        for mword in word.raw_data.find_all("m"):
            if mword['ana'] != " #SUFFIX_NOMINAL_ENDING" and "HIFIL" in mword.get("ana", ""):
                count += 1
                break
    if count > 1:
        print(sent.id)
    bible_mwords = [mword for word in sent.words
                  for mword in word.raw_data.find_all("m") if mword['ana'] != " #SUFFIX_NOMINAL_ENDING"]
    # remove all suffix elements
    sent_words = [convert_word(bible_mword) for bible_mword in bible_mwords]

    for i in range(len(bible_mwords)):
        if "HIFIL" in bible_mwords[i].get("ana", ""):
            hifil_index = i

    return Sentence("Bible", sent.id, hifil_index, sent_words)


def convert_to_unified_sentences(bible_sents = List[BibleSentence]) -> List[Sentence]:
    return [convert_sentence(sent) for sent in bible_sents]


if __name__ == '__main__':
    sentences = Book.get_all_sentences_with_hifeil(["bible_data/Torah.xml", "bible_data/Prophets.xml", "bible_data/Writings.xml"])
    unified_sentences = convert_to_unified_sentences(sentences)
#    Sentence.convert_sentences_to_json(unified_sentences)


