from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base


class MenuItemIngredient(Base):
    """MenuItemIngredient model - many-to-many relationship between menu items and ingredients"""
    __tablename__ = "menu_item_ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity = Column(String(50))  # "200g", "al gusto", etc.
    is_optional = Column(Boolean, default=False)
    
    # Relationships
    menu_item = relationship("MenuItem", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="menu_items")
