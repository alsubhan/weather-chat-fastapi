from pydantic import BaseModel

class Summary(BaseModel):
    id: int
    text: str