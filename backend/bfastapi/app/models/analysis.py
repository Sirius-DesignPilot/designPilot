from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func, JSON
from bfastapi.app.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)

    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    
    title = Column(String(256), nullable=True)

    
    data_input_type = Column(String(50), default="text", nullable=False)

    
    input_text = Column(Text, nullable=True)

    
    geometry = Column(JSON, nullable=True)

   
    errors = Column(JSON, nullable=True)

    
    ai_comment = Column(Text, nullable=True)

   
    result = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
