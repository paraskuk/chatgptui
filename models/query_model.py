from pydantic import BaseModel, Field


class QueryModel(BaseModel):
    user_input: str = Field(min_length=1, max_length=2000)
    model: str = "gpt-4"  # Default model

class FeedbackModel(BaseModel):
    responseId: str
    feedback: str
