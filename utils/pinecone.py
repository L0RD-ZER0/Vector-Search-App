from __future__ import annotations
import pinecone
from utils.config import Config
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from numpy import ndarray


def init_pinecone():
    pinecone.init(api_key=Config.PINECONE_API_KEY, environment=Config.PINECONE_ENVIRONMENT)
    if Config.PINECONE_INDEX not in pinecone.list_indexes():
        create_index()


def create_index():
    pinecone.create_index(Config.PINECONE_INDEX, Config.MODEL_DIMENTIONS, metric='cosine')
    return get_index()


def get_index():
    return pinecone.Index(Config.PINECONE_INDEX)


def upsert_vectors(data: list[dict[str, int | int | ndarray[float]]]):
    data = [(str(_['id']), _['vector'].tolist(), {'mysql_id': _['mysql_id']}) for _ in data]
    get_index().upsert(data)  # type: ignore


def query_pinecone(content_vector: ndarray[float], *, count: int = 10) -> list[dict[str, int | float]]:
    results: pinecone.QueryResponse = get_index().query(vector=content_vector.tolist(), top_k=count, include_metadata=True, include_values=False)  # type: ignore
    results: list = results['matches']
    return [_format_response(_) for _ in results]


def _format_response(data: pinecone.ScoredVector) -> dict[str, int]:
    return {
        'id': int(data['id']),
        'mysql_id': int(data['metadata']['mysql_id']),
        'score': data['score'] * 100,
    }