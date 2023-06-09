from pydantic import BaseModel, Field


class QueryModel(BaseModel):
    user_input: str = Field(min_length=1, max_length=1000)
