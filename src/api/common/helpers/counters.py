from fastapi import Query
from typing import List


def sampling(selection, offset: int, limit: int = Query(default=10, lte=10)) -> List:
    return selection[offset:(limit + offset if limit is not None else None)]