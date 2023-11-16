from typing import Union, List
from pydantic import BaseModel, conlist

class SearchQuery(BaseModel):
    user_query: str
    user_person: str

class DefaultResponseSuccess(BaseModel):
    state: str = "DONE"
    result: Union[dict, list, str]

class DefaultResponseFailure(BaseModel):
    state: str = "FAILED"
    error_msg: str