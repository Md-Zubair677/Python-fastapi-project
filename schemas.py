from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class PostBase(BaseModel):

    title: str = Field( min_length=3, max_length=100)
    author:str= Field( min_length=3, max_length=100)
    content: str = Field( min_length=3, max_length=1000)


class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    
    model_config=ConfigDict(from_attributes=True)

    id: int
    date_posted: str

    
