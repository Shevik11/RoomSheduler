from pydantic import BaseModel

class Days(BaseModel):
    name_group: str
    number_of_subgroup: int
    day_of_week: str
    nominator: str
    time_of_para: str
    namb_of_para: int
    name_of_para: str
    room: str
    teacher: str
    busy: bool

    class Config:
        orm_mode = True
