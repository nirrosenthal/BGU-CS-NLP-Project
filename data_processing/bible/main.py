import tkinter as tk
from tkinter import messagebox
from source.Book import Book
import pandas as pd


def display_unicode_text(input_text: str):
    root = tk.Tk()
    root.title("Display Unicode Text")
    label = tk.Label(root, height=10, width=50, text=input_text)
    label.pack()
    root.mainloop()


if __name__ == '__main__':
    # gets a dict for book and chapter with a list of Sentence Objects
    # sentences = Book.get_all_sentences_with_hifeil(["bible_data/Prophets.xml"])
    sentences = Book.get_all_sentences_with_hifeil(["bible_data/Prophets.xml", "bible_data/Torah.xml", "bible_data/Writings.xml"])
    hifeil_word_col = [str(sen.hifil_word) for sen in sentences]
    pasuk_id_col = [sen.id for sen in sentences]
    pasuk_plain_text_col = [str(sen) for sen in sentences]
    pasuk_raw_data_col = [sen.raw_data for sen in sentences]
    df = pd.DataFrame({'sentence_id': pasuk_id_col,'hifil_word': hifeil_word_col,
                       'pasuk_text': pasuk_plain_text_col, 'xml_raw_data':pasuk_raw_data_col})
    df.to_csv("filtered_bible_sentences.csv", index=False, encoding="utf-8")
