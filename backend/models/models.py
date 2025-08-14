from sqlalchemy import (Boolean, Column, ForeignKey, Integer,
                        PrimaryKeyConstraint, String)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Days(Base):
    __tablename__ = "days_3"

    name_group = Column(String)
    number_of_subgroup = Column(Integer)
    day_of_week = Column(String)
    nominator = Column(String)
    time_of_para = Column(String)
    namb_of_para = Column(Integer)
    name_of_para = Column(String)
    room = Column(String)
    teacher = Column(String)
    busy = Column(Boolean)

    __table_args__ = (
        PrimaryKeyConstraint(
            "name_group", "day_of_week", "namb_of_para", "number_of_subgroup"
        ),
    )
