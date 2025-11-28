from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class IngredientBase(BaseModel):
    """Base schema for Ingredient"""
    name: str = Field(..., min_length=2, max_length=50)
    icon: Optional[str] = Field(None, max_length=10, description="Emoji")
    is_allergen: Optional[bool] = False
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip().title()


class IngredientCreate(IngredientBase):
    """Schema for creating an ingredient"""
    pass


class IngredientUpdate(BaseModel):
    """Schema for updating an ingredient"""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    icon: Optional[str] = None
    is_allergen: Optional[bool] = None


class IngredientResponse(IngredientBase):
    """Schema for ingredient response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class IngredientListResponse(BaseModel):
    """Schema for ingredient list"""
    items: list[IngredientResponse]
    total: int


# Menu Item Ingredient schemas
class MenuItemIngredientBase(BaseModel):
    """Base schema for MenuItemIngredient"""
    ingredient_id: int
    quantity: Optional[str] = Field(None, max_length=50, description="e.g., '200g', 'al gusto'")
    is_optional: Optional[bool] = False


class MenuItemIngredientCreate(MenuItemIngredientBase):
    """Schema for adding ingredient to menu item"""
    pass


class MenuItemIngredientResponse(BaseModel):
    """Schema for menu item ingredient response"""
    id: int
    ingredient_id: int
    ingredient_name: str
    ingredient_icon: Optional[str]
    is_allergen: bool
    quantity: Optional[str]
    is_optional: bool
    
    class Config:
        from_attributes = True
