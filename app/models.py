from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from datetime import datetime
from app.database import Base

class UserPlan(Base):
    __tablename__ = "user_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    weight = Column(Float)
    goal = Column(String)
    intensity = Column(String)
    workout_plan = Column(Text)
    nutrition_tip = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)