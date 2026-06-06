from sqlalchemy import Column, Integer, String
from database import Base

class SnomedFilter(Base):
    __tablename__ = "snomed_filters"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    snomed_descriptor = Column(String, unique=True, index=True, nullable=False)
    icdo_code = Column(String, unique=False, index=False, nullable=False)
    topography = Column(String, unique=False, index=False, nullable=False)
    filter_code = Column(String, unique=False, index=False, nullable=False)
