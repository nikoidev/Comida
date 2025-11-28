from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class CategoryBase(BaseModel):
    """Base schema for Category"""
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    icon: Optional[str] = Field(None, max_length=10, description="Emoji or icon name")
    order: Optional[int] = Field(0, ge=0)
    is_active: Optional[bool] = True
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class CategoryCreate(CategoryBase):
    """Schema for creating a category"""
    restaurant_id: int


class CategoryUpdate(BaseModel):
    """Schema for updating a category"""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = None
    icon: Optional[str] = None
    order: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    """Schema for category response"""
    id: int
    restaurant_id: int
    slug: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class CategoryListResponse(BaseModel):
    """Schema for category list"""
    items: list[CategoryResponse]
    total: int
