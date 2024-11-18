from pydantic import BaseModel


class CategoryShema(BaseModel):
    id: int
    name: str