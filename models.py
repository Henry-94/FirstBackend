from sqlalchemy import Column, Integer, Float
from database import Base

class SoilData(Base):
    __tablename__ = "soil_data"

    id = Column(Integer, primary_key=True, index=True)
    humidity = Column(Float)