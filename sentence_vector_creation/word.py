from enum import Enum


class Number(Enum):
    SINGULAR = 1
    PLURAL = 2
    DUAL = 3
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
    ANY = 4
    NONE = 0


class WordType(Enum):
    ADP = 1
    PROPN = 2
    VERB = 3
    ADJ = 4
    CONJ = 5
    NOUN = 6
    DET = 7
    ADV = 8
    AUX = 9
    PRON = 10

def find_gender(male, female):
    if male == 1:
        return Gender.MALE
    elif female == 1:
        return Gender.FEMALE
    else:
        return Gender.NONE


def find_number(singular, plural, dual):
    if singular == 1:
        return Number.SINGULAR
    elif plural == 1:
        return Number.PLURAL
    elif dual == 1:
        return Number.DUAL
    else:
        return Number.NONE


def find_tense(past, present, future):
    if past == 1:
        return Tense.PAST
    elif present == 1:
        return Tense.PRESENT
    elif future == 1:
        return Tense.FUTURE
    else:
        return Tense.NONE


def find_word_type(adp, propn, verb, adj, conj, noun, det, adv, aux, pron):
    if adp:
        return WordType.ADP
    elif propn:
        return WordType.PROPN
    elif verb:
        return WordType.VERB
    elif adj:
        return WordType.ADJ
    elif conj:
        return WordType.CONJ
    elif noun:
        return WordType.NOUN
    elif det:
        return WordType.DET
    elif adv:
        return WordType.ADV
    elif aux:
        return WordType.AUX
    elif pron:
        return WordType.PRON
    else:
        raise TypeError



def find_person(first, second, third, _any):
    if first == 1:
        return Person.FIRST
    elif second == 1:
        return Person.SECOND
    elif third == 1:
        return Person.THIRD
    elif _any == 1:
        return Person.ANY
    else:
        return Person.NONE


class Word:
    def __init__(self, source: str, word: str, gender: Gender, number: Number, tense: Tense, word_type: WordType, person: Person):
        self._source = source
        self._word = word
        self._male = 1 if gender == Gender.MALE else 0
        self._female = 1 if gender == Gender.FEMALE else 0
        self._singular = 1 if number == Number.SINGULAR else 0
        self._plural = 1 if number == Number.PLURAL else 0
        self._dual = 1 if number == Number.DUAL else 0
        self._tense_past = 1 if tense == Tense.PAST else 0
        self._tense_present = 1 if tense == Tense.PRESENT else 0
        self._tense_future = 1 if tense == Tense.FUTURE else 0
        self._adp = 1 if word_type == WordType.ADP else 0
        self._verb = 1 if word_type == WordType.VERB else 0
        self._adj = 1 if word_type == WordType.ADJ else 0
        self._conj = 1 if word_type == WordType.CONJ else 0
        self._propn = 1 if word_type == WordType.PROPN else 0
        self._pron = 1 if word_type == WordType.PRON else 0
        self._noun = 1 if word_type == WordType.NOUN else 0
        self._det = 1 if word_type == WordType.DET else 0
        self._adv = 1 if word_type == WordType.ADV else 0
        self._aux = 1 if word_type == WordType.AUX else 0
        self._first_person = 1 if person == Person.FIRST else 0
        self._second_person = 1 if person == Person.SECOND else 0
        self._third_person = 1 if person == Person.THIRD else 0
        self._any = 1 if person == Person.ANY else 0

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
    def dual(self):
        return self._dual

    @property
    def past(self):
        return self._tense_past

    @property
    def present(self):
        return self._tense_present

    @property
    def future(self):
        return self._tense_future


    @property
    def adpositional_phrase(self):
        return self._adp

    @property
    def verb(self):
        return self._verb

    @property
    def adjective(self):
        return self._adj

    @property
    def conjunction(self):
        return self._conj

    @property
    def proper_name(self):
        return self._propn

    @property
    def pronoun(self):
        return self._pron

    @property
    def noun(self):
        return self._noun

    @property
    def det(self):
        return self._det

    @property
    def adverb(self):
        return self._adv

    @property
    def auxillery(self):
        return self._aux

    @property
    def first_person(self):
        return self._first_person

    @property
    def second_person(self):
        return self._second_person

    @property
    def third_person(self):
        return self._third_person

    @property
    def any_person(self):
        return self._any

    def properties_dict(self):
        properties = [p for p in dir(self) if not p[0] == "_"]
        properties_dict = {p: self.__getattribute__(p) for p in properties}
        return properties_dict