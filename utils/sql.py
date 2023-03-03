from __future__ import annotations


def init_mysql() -> None:
    """
    Function to initialize MySQL database.

    """
    ...


def upsert_data(article: dict[str, str | int]) -> None:
    """
    Function to update/insert (aka upsert) data into the database.

    Parameters
    ----------
    article: dict[str, str | int]
        The article to insert.
        - article-id: int
        - title: str
        - abstract: str
        - content: str
        - after-word: str
        Any missing keys will either not be present or be valued with `None`
    """
    ...


def query_data(article_id: int) -> dict[str, str | int]:
    """

    Parameters
    ----------
    article_id: int
        ID of Article to fetch.

    Returns
    -------
    dict[str, str | int]
        Article fetched from the database.

    """
    ...


def clean_database() -> None:
    ...
