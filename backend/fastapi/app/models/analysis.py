from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
from app.database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)

    # Analizi yapan kullanıcı
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Analiz edilen veri (metin olabilir)
    input_text = Column(Text, nullable=False)

    # AI modelinden dönen sonuç
    result = Column(Text, nullable=True)

    # oluşturulma tarihi
    created_at = Column(DateTime(timezone=True), server_default=func.now())
