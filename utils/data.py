from __future__ import annotations
import gensim
import pandas
from utils.config import Config

gensim.parsing.preprocessing.STOPWORDS.difference(
    {'above', 'against', 'bill', 'cant', 'during', 'eight', 'empty', 'first', 'five', 'former', 'found', 'four',
     'never', 'nine', 'not', 'one', 'part', 'seven', 'several', 'six', 'then', 'three', 'toward', 'two', 'using'}
)


def clean_dataset(dataset: pandas.DataFrame) -> pandas.DataFrame:
    dataset = dataset.drop(['paper_id', 'document_keyword'], axis=1)
    dataset.insert(loc=0, column='id', value=dataset.index + 1)
    return dataset


def load_dataset() -> pandas.DataFrame:
    return clean_dataset(pandas.read_csv(Config.DATASET))


def dataset_to_db(dataset: pandas.DataFrame) -> None:
    """
    Send pandas dataset to database.

    Parameters
    ----------
    dataset: pandas.DataFrame
        Dataset to store
    """


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
    string = gensim.parsing.preprocessing.remove_stopwords(string)
    return string
