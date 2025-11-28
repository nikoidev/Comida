from sqlalchemy.orm import Session
from slugify import slugify
from typing import Optional, List
from ..models.restaurant import Restaurant
from ..schemas.restaurant import RestaurantCreate, RestaurantUpdate


class RestaurantService:
    """Service class for Restaurant business logic"""
    
    @staticmethod
    def create_restaurant(db: Session, restaurant: RestaurantCreate, user_id: int) -> Restaurant:
        """Create a new restaurant"""
        # Generate slug from name
        slug = slugify(restaurant.name)
        
        # Ensure unique slug
        base_slug = slug
        counter = 1
        while db.query(Restaurant).filter(Restaurant.slug == slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        db_restaurant = Restaurant(
            **restaurant.dict(),
            user_id=user_id,
            slug=slug
        )
        db.add(db_restaurant)
        db.commit()
        db.refresh(db_restaurant)
        return db_restaurant
    
    @staticmethod
    def get_restaurant(db: Session, restaurant_id: int) -> Optional[Restaurant]:
        """Get restaurant by ID"""
        return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    
    @staticmethod
    def get_restaurant_by_slug(db: Session, slug: str) -> Optional[Restaurant]:
        """Get restaurant by slug (for public site)"""
        return db.query(Restaurant).filter(
            Restaurant.slug == slug,
            Restaurant.is_published == True
        ).first()
    
    @staticmethod
    def get_user_restaurants(db: Session, user_id: int) -> List[Restaurant]:
        """Get all restaurants owned by a user"""
        return db.query(Restaurant).filter(Restaurant.user_id == user_id).all()
    
    @staticmethod
    def update_restaurant(
        db: Session, 
        restaurant_id: int, 
        restaurant: RestaurantUpdate
    ) -> Optional[Restaurant]:
        """Update restaurant"""
        db_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if not db_restaurant:
            return None
        
        update_data = restaurant.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_restaurant, field, value)
        
        db.commit()
        db.refresh(db_restaurant)
        return db_restaurant
    
    @staticmethod
    def delete_restaurant(db: Session, restaurant_id: int) -> bool:
        """Delete restaurant"""
        db_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if db_restaurant:
            db.delete(db_restaurant)
            db.commit()
            return True
        return False
    
    @staticmethod
    def publish_restaurant(db: Session, restaurant_id: int, is_published: bool) -> Optional[Restaurant]:
        """Publish or unpublish restaurant"""
        db_restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
        if db_restaurant:
            db_restaurant.is_published = is_published
            db.commit()
            db.refresh(db_restaurant)
            return db_restaurant
        return None
    
    @staticmethod
    def check_ownership(restaurant: Restaurant, user_id: int, is_superuser: bool = False) -> bool:
        """Check if user owns the restaurant"""
        return restaurant.user_id == user_id or is_superuser
