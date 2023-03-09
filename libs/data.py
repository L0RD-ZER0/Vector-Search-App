from __future__ import annotations

from typing import TypedDict, Optional

import gensim
import pandas

from libs.config import Config

gensim.parsing.preprocessing.STOPWORDS.difference(
    {'above', 'against', 'bill', 'cant', 'during', 'eight', 'empty', 'first', 'five', 'former', 'found', 'four',
     'never', 'nine', 'not', 'one', 'part', 'seven', 'several', 'six', 'then', 'three', 'toward', 'two', 'using'}
)

RECORD = TypedDict('RECORD', {
    'id': int,
    'title': str,
    'authors': Optional[str],
    'affiliations': Optional[str],
    'abstract': Optional[str],
    'text': str,
    'bibliography': str,
})


def create_vector_text(record: pandas.Series | RECORD):
    return record['title'] + " \n\n" + record['text']


def clean_dataset(dataset: pandas.DataFrame) -> pandas.DataFrame:
    dataset.drop(['paper_id', 'document_keyword'], axis=1, inplace=True)
    dataset.dropna(subset=['title'], axis=0, inplace=True)
    dataset.insert(loc=0, column='id', value=range(1, 1 + len(dataset), 1))  # type: ignore
    dataset.index = range(0, len(dataset))
    return dataset


def load_dataset() -> pandas.DataFrame:
    return clean_dataset(pandas.read_csv(Config.DATASET))


def normalise_string(string: str) -> str:
    """
    Function to normalise a string of character casing, stopwords, etc.

    Parameters
    ----------
    string: str
        String to normalise

    Returns
    -------
    str
        Normalised string.

    """
    string = string.lower()
    # string = gensim.parsing.preprocessing.remove_stopwords(string)  # remove stopwords
    return string
