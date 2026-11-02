from pydantic import BaseModel


class ExhibitInputSchema(BaseModel):
    title: str
    description: str
    history: str
    origin: str
    image_url: str

class ExhibitOutSchema(BaseModel):
    id: int
    title: str
    description: str
    history: str
    origin: str
    image_url: str
