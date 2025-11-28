from pydantic import BaseModel, Field, validator
from typing import Optional, Dict
from datetime import datetime
import re


class RestaurantBase(BaseModel):
    """Base schema for Restaurant"""
    name: str = Field(..., min_length=3, max_length=100, description="Restaurant name")
    description: Optional[str] = Field(None, max_length=1000)
    phone: Optional[str] = Field(None, max_length=20)
    whatsapp: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    opening_hours: Optional[Dict[str, str]] = None
    primary_color: Optional[str] = Field("#DC143C", pattern=r"^#[0-9A-Fa-f]{6}$")
    secondary_color: Optional[str] = Field("#228B22", pattern=r"^#[0-9A-Fa-f]{6}$")
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class RestaurantCreate(RestaurantBase):
    """Schema for creating a restaurant"""
    pass


class RestaurantUpdate(BaseModel):
    """Schema for updating a restaurant"""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    logo_url: Optional[str] = None
    cover_image_url: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    opening_hours: Optional[Dict[str, str]] = None
    primary_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    secondary_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    template_id: Optional[int] = None
    meta_title: Optional[str] = Field(None, max_length=60)
    meta_description: Optional[str] = Field(None, max_length=160)
    is_published: Optional[bool] = None


class RestaurantResponse(RestaurantBase):
    """Schema for restaurant response"""
    id: int
    user_id: int
    slug: str
    logo_url: Optional[str]
    cover_image_url: Optional[str]
    template_id: int
    meta_title: Optional[str]
    meta_description: Optional[str]
    is_published: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class RestaurantListResponse(BaseModel):
    """Schema for paginated restaurant list"""
    items: list[RestaurantResponse]
    total: int
    page: int
    pages: int
