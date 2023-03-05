from __future__ import annotations
import pinecone
from utils.config import Config
import numpy


def init_pinecone():
    pinecone.init(api_key=Config.PINECONE_API_KEY, environment=Config.PINECONE_ENVIRONMENT)
    if Config.PINECONE_INDEX not in pinecone.list_indexes():
        create_index()


def create_index():
    pinecone.create_index(Config.PINECONE_INDEX, Config.MODEL_DIMENTIONS, metric='cosine')
    return get_index()


def get_index():
    return pinecone.Index(Config.PINECONE_INDEX)


def upsert_vectors(data: list[dict[str, int | int | numpy.ndarray[float]]], *, batch_size: int = 100):
    data = [(str(_['id']), _['vector'].tolist(), {'mysql_id': _['mysql_id']}) for _ in data]
    for batch_start in range(0, len(data), batch_size):
        get_index().upsert(data[batch_start: batch_start + batch_size])  # type: ignore


def upsert_vector(data: dict[str, int | int | numpy.ndarray[float]]):
    upsert_vectors([data])


def query_pinecone(content_vector: numpy.ndarray[float], *, count: int = 10) -> list[dict[str, int | float]]:
    results: pinecone.QueryResponse = get_index().query(vector=content_vector.tolist(), top_k=count, include_metadata=True, include_values=False)  # type: ignore
    results: list = results['matches']
    return [_format_query_response(_) for _ in results]


def _format_query_response(data: pinecone.ScoredVector) -> dict[str, int]:
    return {
        'id': int(data['id']),
        'mysql_id': int(data['metadata']['mysql_id']),
        'score': data['score'] * 100,
    }


def query_articles(article_ids: list[int]):
    response: pinecone.FetchResult = get_index().fetch(ids=[str(article_id) for article_id in article_ids])
    results = []
    for result in response['vectors'].values():
        results.append(_format_fetch_response(result))
    return results


def query_article(article_id: int):
    d = query_articles([article_id])
    return d[0] if d else None


def _format_fetch_response(data: dict[str, str | dict[str | int] | list[float]]):
    return {
        'id': int(data['id']),
        'mysql_id': int(data['metadata']['mysql_id']),
        'vector': numpy.array(data['values']),
    }
