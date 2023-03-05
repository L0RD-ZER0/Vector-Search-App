from __future__ import annotations

from mysql import connector

from libs.config import Config

_CONNECTION: connector.CMySQLConnection | None = None
_DATABASE = '`plagiarism_analysis`'
_TABLES = {
    'reports': """
    CREATE TABLE IF NOT EXISTS `reports`(
        `id` int(15) PRIMARY KEY,
        `title` varchar(4095) NOT NULL,
        `authors` varchar(4095),
        `affiliations` mediumtext,
        `abstract` mediumtext,
        `text` mediumtext NOT NULL,
        `bibliography` mediumtext NOT NULL
    );
    """
}

_QUERIES = {
    'insert_article': """
        INSERT INTO `reports` (
            `id`, 
            `title`, 
            `authors`, 
            `affiliations`, 
            `abstract`, 
            `text`, 
            `bibliography`
        )
        VALUES(
            %(id)s,
            %(title)s,
            %(authors)s,
            %(affiliations)s,
            %(abstract)s,
            %(text)s,
            %(bibliography)s
        )
        ON DUPLICATE KEY UPDATE
            `title` = VALUES(`title`),
            `authors` = VALUES(`authors`),
            `affiliations` = VALUES(`affiliations`),
            `abstract` = VALUES(`abstract`),
            `text` = VALUES(`text`),
            `bibliography` = VALUES(`bibliography`);
    
    """,
    'fetch_article': """
    SELECT `id`, `title`, `authors`, `affiliations`, `abstract`, `text`, `bibliography`
    FROM 
        `reports`
    WHERE
        `id` = %(id)s
    ;
    """,
    'clear_articles': """
    DELETE FROM `reports`
    """,
    'fetch_title': """
    SELECT `id`, `title`
    FROM 
        `reports`
    WHERE
        `id` = %(id)s
    ;
    """
}


def init_mysql() -> None:
    """
    Function to initialize MySQL database.
    """
    global _CONNECTION
    _CONNECTION = connector.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWD,
    )
    cur = _CONNECTION.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {_DATABASE};")
    cur.execute(f"USE {_DATABASE};")
    for table in (tables := get_tables()):
        cur.execute(tables[table])
    _CONNECTION.commit()
    cur.close()


def get_tables():
    return _TABLES.copy()


def get_connection():
    return _CONNECTION


def upsert_article(
        data: dict[str, int | str | None]
) -> None:
    """
    Helper to update/insert (aka upsert) data into the database.

    Parameters
    ----------
    data: dict[str, str | int | None
        Data to be inserted. Has the following fields:
          - article_id: ID of article
          - title: Title of article
          - authors: Authors of article
          - affiliations: Affiliations of article
          - abstract: Abstract of article
          - text: Content of article
          - bibliography: Bibliography of article
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_QUERIES['insert_article'], data)
    conn.commit()
    cur.close()


def upsert_articles(data: list[dict[str, int | str | None]]):
    conn = get_connection()
    cur = conn.cursor()
    cur.executemany(_QUERIES['insert_article'], data)
    conn.commit()
    cur.close()


def query_article(article_id: int) -> dict[str, str | int]:
    """
    Function to get article by id.

    Parameters
    ----------
    article_id: int
        ID of Article to fetch.

    Returns
    -------
    dict[str, str | int]
        Article fetched from the database.

    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_QUERIES['fetch_article'], {'id': article_id})
    data = cur.fetchall()[0]
    data = {
        'id': data[0],
        'title': data[1],
        'authors': data[2],
        'affiliations': data[3],
        'abstract': data[4],
        'text': data[5],
        'bibliography': data[6],
    }
    cur.close()
    return data


def query_articles(article_ids: list[int]) -> list[dict[str, str | int]]:
    """
    Function to get articles by id.

    Parameters
    ----------
    article_ids: int
        List of IDs of Articles to fetch.

    Returns
    -------
    list[dict[str, str | int]]
        List of article fetched from the database.

    """
    data = []
    for article_id in article_ids:
        data.append(query_article(article_id))
    return data


def fetch_title(article_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_QUERIES['fetch_article'], {'id': article_id})
    data = cur.fetchall()[0]
    data = {
        'id': data[0],
        'title': data[1],
    }
    cur.close()
    return data


def fetch_titles(article_ids: list[int]):
    data = []
    for article_id in article_ids:
        data.append(fetch_title(article_id))
    return data


def clean_database() -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_QUERIES['clear_articles'])
    conn.commit()
    cur.close()


def teardown_mysql():
    global _CONNECTION
    _CONNECTION.close()
    del _CONNECTION
