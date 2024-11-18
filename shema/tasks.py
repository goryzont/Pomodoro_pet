from pydantic import BaseModel, Field, model_validator

class TaskShema(BaseModel):
    id: int | None = None
    name: str | None = None
    pomidoro_count: int | None = None
    category_id: int  #    = Field(exclude=True)
    user_id: int | None = None

    class Config:
        from_attributes = True


    @model_validator(mode='after')
    def check_name_of_pomidoro_count_is_not_none(self):
        if self.name is None and self.pomidoro_count is None:
            raise ValueError('name and pomidoro-count was provided')
        return self


class TaskCreateShema(BaseModel):
    name: str | None = None
    pomidoro_count: int | None = None
    category_id: int