from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Restaurant(Base):
    """Restaurant model - represents a food business"""
    __tablename__ = "restaurants"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Basic info
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    logo_url = Column(String(500))
    cover_image_url = Column(String(500))
    
    # Contact
    phone = Column(String(20))
    whatsapp = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    
    # Business hours (JSON: {"monday": "9:00-22:00", "tuesday": "9:00-22:00", ...})
    opening_hours = Column(JSON)
    
    # Template & styling
    template_id = Column(Integer, default=1)  # Default template
    primary_color = Column(String(7), default="#DC143C")  # Hex color
    secondary_color = Column(String(7), default="#228B22")
    
    # SEO
    meta_title = Column(String(60))
    meta_description = Column(String(160))
    
    # Status
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="restaurants")
    categories = relationship("Category", back_populates="restaurant", cascade="all, delete-orphan")
    menu_items = relationship("MenuItem", back_populates="restaurant", cascade="all, delete-orphan")
