from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from bd import Base


class Days(Base):
    __tablename__ = "days"

    name_group = Column(String, primary_key=True)
    number_of_subgroup = Column(Integer)
    day_of_week = Column(String)
    nominator = Column(String)
    time_of_para = Column(String,)
    namb_of_para = Column(Integer)
    name_of_para = Column(String)
    room = Column(String)
    teacher = Column(String)
    busy = Column(Boolean)

    class Config:
        orm_mode = True