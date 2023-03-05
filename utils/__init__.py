from __future__ import annotations
from typing import TYPE_CHECKING, TypedDict, Optional

from utils import pinecone, sql, vectorisation

if TYPE_CHECKING:
    from numpy import ndarray
    from pandas import Series


_INPUT = vectorisation.RECORD


def init():
    pinecone.init_pinecone()
    sql.init_mysql()
    vectorisation.init_vectoriser()


def validate_input(inp: _INPUT):
    if 'id' not in inp:
        inp['id'] = pinecone.get_count() + 1
    for k in 'title', 'text', 'bibliography':
        assert k in inp, f"Key: `{k}` is not in input."
    for k in 'authors', 'affiliations', 'abstract':
        inp[k] = inp.get(k, None)  # type: ignore


def upsert_article(data: _INPUT):
    validate_input(data)
    vector = vectorisation.create_vector_text(data)
    vector = vectorisation.vectorise(vector)
    vector = {'id': data['id'], 'mysql_id': data['id'], 'vector': vector}
    pinecone.upsert_vector(vector)
    sql.upsert_article(data)


def upsert_articles(data: list[_INPUT]):
    for __, _ in enumerate(data):
        assert 'id' in _, f"Key: `id` is not in input for index {__}."
        validate_input(_)
    vectors = [vectorisation.create_vector_text(_) for _ in data]
    vectors = vectorisation.vectorise_many(vectors)
    vectors = [
        {'id': data[i]['id'], 'mysql_id': data[i]['id'], 'vector': vectors[i]}
        for i in range(len(data))
    ]
    pinecone.upsert_vectors(vectors)
    sql.upsert_articles(data)


def fetch_article(article_id: int, *, include_vector: bool = False) -> dict[str, int | str | ndarray | None]:
    data = sql.query_article(article_id)
    if include_vector:
        vector_data = pinecone.query_article(article_id)
        data['vector'] = vector_data['vector']
    return data


def fetch_articles(
        article_ids: list[int],
        # *,
        # include_vectors: bool = False
) -> list[dict[str, int | str | ndarray | None]]:
    data = sql.query_articles(article_ids)
    # if include_vectors:
    #     vectors = pinecone.query_articles(article_ids)
    return data


def fetch_title(article_id: int) -> dict[str, int | str]:
    return sql.fetch_title(article_id)


def fetch_titles(article_ids: list[int]) -> list[dict[str, int | str]]:
    return sql.fetch_titles(article_ids)


def check_article(data: dict[str, int | str | None]) -> list[dict[str, int | str | None]]:
    assert 'title' in data
    assert 'text' in data
    query = vectorisation.normalise_string(vectorisation.create_vector_text(data))
    query_vector = vectorisation.vectorise(query)
    results = pinecone.query_pinecone(query_vector)
    return results


def analyse_article(data: dict[str, int | str | None], *, titles_only: bool = True):
    assert 'title' in data
    assert 'text' in data
    query_results = check_article(data)
    for res in query_results:
        if titles_only:
            record = fetch_title(res['mysql_id'])
        else:
            record = fetch_article(article_id=res['mysql_id'])
        del res['mysql_id']
        res.update(record)
    return query_results


def teardwn():
    pinecone.teardown_pinecone()
    sql.teardown_mysql()
    vectorisation.teardown_vectoriser()
