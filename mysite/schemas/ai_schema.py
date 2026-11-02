from pydantic import BaseModel


class AskInputSchema(BaseModel):
    question: str

class AskOutputSchema(BaseModel):
    answer: str
