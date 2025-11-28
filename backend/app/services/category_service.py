from sqlalchemy.orm import Session
from slugify import slugify
from typing import Optional, List
from ..models.category import Category
from ..schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    """Service class for Category business logic"""
    
    @staticmethod
    def create_category(db: Session, category: CategoryCreate) -> Category:
        """Create a new category"""
        # Generate slug from name
        slug = slugify(category.name)
        
        # Ensure unique slug within restaurant
        base_slug = slug
        counter = 1
        while db.query(Category).filter(
            Category.restaurant_id == category.restaurant_id,
            Category.slug == slug
        ).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        db_category = Category(
            **category.dict(),
            slug=slug
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    
    @staticmethod
    def get_category(db: Session, category_id: int) -> Optional[Category]:
        """Get category by ID"""
        return db.query(Category).filter(Category.id == category_id).first()
    
    @staticmethod
    def get_restaurant_categories(
        db: Session, 
        restaurant_id: int,
        active_only: bool = False
    ) -> List[Category]:
        """Get all categories for a restaurant"""
        query = db.query(Category).filter(Category.restaurant_id == restaurant_id)
        
        if active_only:
            query = query.filter(Category.is_active == True)
        
        return query.order_by(Category.order, Category.name).all()
    
    @staticmethod
    def update_category(
        db: Session, 
        category_id: int, 
        category: CategoryUpdate
    ) -> Optional[Category]:
        """Update category"""
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if not db_category:
            return None
        
        update_data = category.dict(exclude_unset=True)
        
        # Update slug if name changed
        if 'name' in update_data:
            update_data['slug'] = slugify(update_data['name'])
        
        for field, value in update_data.items():
            setattr(db_category, field, value)
        
        db.commit()
        db.refresh(db_category)
        return db_category
    
    @staticmethod
    def delete_category(db: Session, category_id: int) -> bool:
        """Delete category"""
        db_category = db.query(Category).filter(Category.id == category_id).first()
        if db_category:
            db.delete(db_category)
            db.commit()
            return True
        return False
    
    @staticmethod
    def reorder_categories(db: Session, category_orders: List[dict]) -> bool:
        """Reorder categories - expects list of {id: int, order: int}"""
        try:
            for item in category_orders:
                db_category = db.query(Category).filter(Category.id == item['id']).first()
                if db_category:
                    db_category.order = item['order']
            db.commit()
            return True
        except Exception:
            db.rollback()
            return False
