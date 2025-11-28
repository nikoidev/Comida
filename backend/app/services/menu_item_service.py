from sqlalchemy.orm import Session
from slugify import slugify
from typing import Optional, List
from ..models.menu_item import MenuItem
from ..schemas.menu_item import MenuItemCreate, MenuItemUpdate


class MenuItemService:
    """Service class for MenuItem business logic"""
    
    @staticmethod
    def create_menu_item(db: Session, menu_item: MenuItemCreate) -> MenuItem:
        """Create a new menu item"""
        # Generate slug from name
        slug = slugify(menu_item.name)
        
        # Ensure unique slug within restaurant
        base_slug = slug
        counter = 1
        while db.query(MenuItem).filter(
            MenuItem.restaurant_id == menu_item.restaurant_id,
            MenuItem.slug == slug
        ).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        db_menu_item = MenuItem(
            **menu_item.dict(),
            slug=slug
        )
        db.add(db_menu_item)
        db.commit()
        db.refresh(db_menu_item)
        return db_menu_item
    
    @staticmethod
    def get_menu_item(db: Session, menu_item_id: int) -> Optional[MenuItem]:
        """Get menu item by ID"""
        return db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    
    @staticmethod
    def get_menu_item_by_slug(db: Session, restaurant_id: int, slug: str) -> Optional[MenuItem]:
        """Get menu item by slug (for public site)"""
        return db.query(MenuItem).filter(
            MenuItem.restaurant_id == restaurant_id,
            MenuItem.slug == slug,
            MenuItem.is_available == True
        ).first()
    
    @staticmethod
    def get_restaurant_menu_items(
        db: Session,
        restaurant_id: int,
        category_id: Optional[int] = None,
        available_only: bool = False,
        featured_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[MenuItem], int]:
        """Get menu items for a restaurant with filters"""
        query = db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id)
        
        if category_id:
            query = query.filter(MenuItem.category_id == category_id)
        
        if available_only:
            query = query.filter(MenuItem.is_available == True)
        
        if featured_only:
            query = query.filter(MenuItem.is_featured == True)
        
        total = query.count()
        items = query.order_by(MenuItem.order, MenuItem.name).offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def update_menu_item(
        db: Session,
        menu_item_id: int,
        menu_item: MenuItemUpdate
    ) -> Optional[MenuItem]:
        """Update menu item"""
        db_menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
        if not db_menu_item:
            return None
        
        update_data = menu_item.dict(exclude_unset=True)
        
        # Update slug if name changed
        if 'name' in update_data:
            update_data['slug'] = slugify(update_data['name'])
        
        for field, value in update_data.items():
            setattr(db_menu_item, field, value)
        
        db.commit()
        db.refresh(db_menu_item)
        return db_menu_item
    
    @staticmethod
    def delete_menu_item(db: Session, menu_item_id: int) -> bool:
        """Delete menu item"""
        db_menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
        if db_menu_item:
            db.delete(db_menu_item)
            db.commit()
            return True
        return False
    
    @staticmethod
    def toggle_availability(db: Session, menu_item_id: int) -> Optional[MenuItem]:
        """Toggle menu item availability"""
        db_menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
        if db_menu_item:
            db_menu_item.is_available = not db_menu_item.is_available
            db.commit()
            db.refresh(db_menu_item)
            return db_menu_item
        return None
    
    @staticmethod
    def toggle_featured(db: Session, menu_item_id: int) -> Optional[MenuItem]:
        """Toggle menu item featured status"""
        db_menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
        if db_menu_item:
            db_menu_item.is_featured = not db_menu_item.is_featured
            db.commit()
            db.refresh(db_menu_item)
            return db_menu_item
        return None
