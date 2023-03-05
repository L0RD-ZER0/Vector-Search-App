from __future__ import annotations
from typing import TYPE_CHECKING
from sentence_transformers import SentenceTransformer
from utils.config import Config
from utils.data import normalise_string

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
