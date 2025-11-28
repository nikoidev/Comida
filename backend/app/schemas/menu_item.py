from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal


class MenuItemBase(BaseModel):
    """Base schema for MenuItem"""
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    currency: Optional[str] = Field("USD", min_length=3, max_length=3)
    preparation_time: Optional[int] = Field(None, ge=0, description="Preparation time in minutes")
    serves: Optional[int] = Field(None, ge=1, description="Number of servings")
    calories: Optional[int] = Field(None, ge=0)
    is_vegetarian: Optional[bool] = False
    is_vegan: Optional[bool] = False
    is_gluten_free: Optional[bool] = False
    is_spicy: Optional[bool] = False
    spicy_level: Optional[int] = Field(0, ge=0, le=5)
    is_available: Optional[bool] = True
    is_featured: Optional[bool] = False
    order: Optional[int] = Field(0, ge=0)
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @validator('currency')
    def validate_currency(cls, v):
        if v:
            return v.upper()
        return v


class MenuItemCreate(MenuItemBase):
    """Schema for creating a menu item"""
    restaurant_id: int
    category_id: int


class MenuItemUpdate(BaseModel):
    """Schema for updating a menu item"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[Decimal] = Field(None, gt=0)
    currency: Optional[str] = None
    preparation_time: Optional[int] = Field(None, ge=0)
    serves: Optional[int] = Field(None, ge=1)
    calories: Optional[int] = Field(None, ge=0)
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_gluten_free: Optional[bool] = None
    is_spicy: Optional[bool] = None
    spicy_level: Optional[int] = Field(None, ge=0, le=5)
    is_available: Optional[bool] = None
    is_featured: Optional[bool] = None
    order: Optional[int] = Field(None, ge=0)


class MenuItemResponse(MenuItemBase):
    """Schema for menu item response"""
    id: int
    restaurant_id: int
    category_id: int
    slug: str
    image_url: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class MenuItemListResponse(BaseModel):
    """Schema for paginated menu item list"""
    items: list[MenuItemResponse]
    total: int
    page: int
    pages: int
