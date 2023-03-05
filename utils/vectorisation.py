from __future__ import annotations
from typing import TYPE_CHECKING
from sentence_transformers import SentenceTransformer
from utils.config import Config
from utils.data import normalise_string, RECORD, create_vector_text

if TYPE_CHECKING:
    from numpy import ndarray


_MODEL: SentenceTransformer | None = None


def init_vectoriser():
    global _MODEL
    _MODEL = SentenceTransformer(Config.MODEL_NAME)


def vectorise(string: str) -> ndarray[float]:
    string = normalise_string(string)
    vector = _MODEL.encode([string])
    return vector[0]


def vectorise_many(strings: list[str], *, batch_size=50) -> list[ndarray[float]]:
    strings = [normalise_string(string) for string in strings]
    vectors = _MODEL.encode(strings, batch_size=batch_size)
    return vectors


def teardown_vectoriser():
    global _MODEL
    del _MODEL
    _MODEL = None
