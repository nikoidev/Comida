from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Ingredient(Base):
    """Ingredient model - represents an ingredient that can be used in menu items"""
    __tablename__ = "ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    icon = Column(String(10))  # Emoji
    is_allergen = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    menu_items = relationship("MenuItemIngredient", back_populates="ingredient")
