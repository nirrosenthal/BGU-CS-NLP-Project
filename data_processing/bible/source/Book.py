import os.path

from bs4 import BeautifulSoup
from typing import List

from Chapter import Chapter
from enum import Enum


class BookGroup(Enum):
    Prophets = "Prophets"
    Torah = "Torah"
    Writings = "Writings"


class Book:
    def __init__(self, book_group: BookGroup, raw_book_data: BeautifulSoup):
        self._book_group = book_group
        self._raw_book_data = raw_book_data
        self._id = raw_book_data.find("div1").get("xml:id")
        self._chapters = [Chapter(raw_chapter_data) for raw_chapter_data in raw_book_data.find_all("div2")]

    @property
    def book_group(self):
        return self._book_group

    @property
    def raw_book_data(self):
        return self._raw_book_data

    @property
    def id(self):
        return self._id

    @property
    def chapters(self):
        return self._chapters

    @classmethod
    def load_xml_book(cls, path: str) -> BeautifulSoup:
        with open(path, 'r', encoding="utf8") as f:
            data = f.read()
        return BeautifulSoup(data, 'xml')

    def get_sentences_with_hifeil(self) -> List['Sentences']:
        # sents = [s for chapter in self._chapters for s in chapter.sentences]
        # s = len(sents[0].words)+0.0
        # for i in range(1, len(sents)-1):
        #     s = float(s*i)/(i+1)+float(len(sents[i].words))/(i+1)
        # print("total\t"+str(len(sents))+"\tavg_len\t"+str(s))
        return [sen for chapter in self._chapters for sen in chapter.get_sentences_with_hifeil()]

    @staticmethod
    def _xml_paths_list(book_group_xml_paths: str or list(str)) -> List[str]:
        if isinstance(book_group_xml_paths, str):
            return [book_group_xml_paths]
        else:
            return book_group_xml_paths

    @staticmethod
    def _get_book_from_book_body(book_group: BookGroup, group_path_data:str, book_body: str) -> 'Book':
        book_path: str = book_body.get("xlink:href").split("#")[0]
        abs_book_path = os.path.join(group_path_data, book_path)
        return Book(book_group, Book.load_xml_book(abs_book_path))

    @classmethod
    def get_all_sentences_with_hifeil(cls, book_group_xml_paths: str or list(str)) -> List['Sentence']:
        sentences = []
        for book_group_xml_path in Book._xml_paths_list(book_group_xml_paths):
            group_book_data: BeautifulSoup = Book.load_xml_book(book_group_xml_path)
            book_group = BookGroup(group_book_data.find("text").get("DisplayName_Eng"))
            group_path_data = book_group_xml_path.split("/")[0]

            for book_body in group_book_data.find_all("body"):
                book = Book._get_book_from_book_body(book_group, group_path_data, book_body)
                sentences += book.get_sentences_with_hifeil()
        return sentences

