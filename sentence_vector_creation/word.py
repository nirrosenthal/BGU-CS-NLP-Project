class Word:
    def __init__(self, source, raw_data):
        self._source = source
        self._raw_data = raw_data
        # set default values-
        self._gender = 0
        self._number = 0
        # times
        self._time_past = 1
        self._time_present = 0
        self._time_future = 0
        # word type
        self._adp = 0
        self._verb = 0
        self._noun = 0
        self._name = 0
        self._adjective = 0
        # person type
        self._first_person = 0
        self._second_person = 0
        self._third_person = 0
        # set values based on type of raw data
        self._set_values()


    @property
    def gender(self):
        return self._gender

    @property
    def number(self):
        return self._number

    @property
    def time_past(self):
        return self._time_past

    @property
    def time_present(self):
        return self._time_present

    @property
    def time_future(self):
        return self._time_future

    @property
    def adp(self):
        return self._adp

    @property
    def verb(self):
        return self._verb

    @property
    def noun(self):
        return self._noun

    @property
    def name(self):
        return self._name

    @property
    def adjective(self):
        return self._adjective

    @property
    def first_person(self):
        return self._first_person

    @property
    def second_person(self):
        return self._second_person

    @property
    def third_person(self):
        return self._third_person

    def _set_values(self):
        if self._source == "Bible":
            self.set_bible_values()
        elif self._source == "Modern":
            self.set_modern_hebrew_values()
        else:
            raise TypeError

    def _set_bible_values(self):
        raise NotImplementedError

    def _set_modern_hebrew_values(self):
        raise NotImplementedError