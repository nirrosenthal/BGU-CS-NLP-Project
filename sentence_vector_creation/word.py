from enum import Enum


class Number(Enum):
    SINGULAR = 1
    PLURAL = 2
    NONE = 0


class Gender(Enum):
    MALE = 1
    FEMALE = 2
    NONE = 0


class Tense(Enum):
    PAST = 1
    PRESENT = 2
    FUTURE = 3
    NONE = 0


class Person(Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    NONE = 0


class WordType(Enum):
    ADP = 1
    PROPN = 2
    VERB = 3
    ADJ = 4
    CONJ = 5


class Word:
    def __init__(self, source: str, word: str, gender: Gender, number: Number, tense: Tense,
                 word_type: WordType, person: Person):
        self._source = source
        self._word = word
        self._male = 1 if gender == Gender.MALE else 0
        self._female = 1 if gender == Gender.FEMALE else 0
        self._singular = 1 if number == Number.SINGULAR else 0
        self._plural = 1 if number == Number.PLURAL else 0
        self._tense_past = 1 if tense == Tense.PAST else 0
        self._tense_present = 1 if tense == Tense.PRESENT else 0
        self._tense_future = 1 if tense == Tense.FUTURE else 0
        self._adp = 1 if word_type == WordType.ADP else 0
        self._verb = 1 if word_type == WordType.VERB else 0
        self._adj = 1 if word_type == WordType.ADJ else 0
        self._conj = 1 if word_type == WordType.CONJ else 0
        self._propn = 1 if word_type == WordType.PROPN else 0
        self._first_person = 1 if person == Person.FIRST else 0
        self._second_person = 1 if person == Person.SECOND else 0
        self._third_person = 1 if person == Person.Third else 0

    @property
    def male(self):
        return self._male

    @property
    def female(self):
        return self._female

    @property
    def singular(self):
        return self._singular

    @property
    def plural(self):
        return self._plural

    @property
    def time_past(self):
        return self._tense_past

    @property
    def time_present(self):
        return self._tense_present

    @property
    def time_future(self):
        return self._tense_future

    @property
    def adpositional_phrase(self):
        return self._adp

    @property
    def verb(self):
        return self._verb

    @property
    def proper_name(self):
        return self._propn

    @property
    def adjective(self):
        return self._adj

    @property
    def conjunction(self):
        return self._conj

    @property
    def first_person(self):
        return self._first_person

    @property
    def second_person(self):
        return self._second_person

    @property
    def third_person(self):
        return self._third_person
