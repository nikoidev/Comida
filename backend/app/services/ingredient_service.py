from sqlalchemy.orm import Session
from typing import Optional, List
from ..models.ingredient import Ingredient
from ..models.menu_item_ingredient import MenuItemIngredient
from ..schemas.ingredient import IngredientCreate, IngredientUpdate


class IngredientService:
    """Service class for Ingredient business logic"""
    
    @staticmethod
    def create_ingredient(db: Session, ingredient: IngredientCreate) -> Ingredient:
        """Create a new ingredient"""
        db_ingredient = Ingredient(**ingredient.dict())
        db.add(db_ingredient)
        db.commit()
        db.refresh(db_ingredient)
        return db_ingredient
    
    @staticmethod
    def get_ingredient(db: Session, ingredient_id: int) -> Optional[Ingredient]:
        """Get ingredient by ID"""
        return db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    
    @staticmethod
    def get_ingredient_by_name(db: Session, name: str) -> Optional[Ingredient]:
        """Get ingredient by name"""
        return db.query(Ingredient).filter(Ingredient.name.ilike(name)).first()
    
    @staticmethod
    def get_all_ingredients(
        db: Session,
        allergens_only: bool = False,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Ingredient], int]:
        """Get all ingredients with optional filtering"""
        query = db.query(Ingredient)
        
        if allergens_only:
            query = query.filter(Ingredient.is_allergen == True)
        
        total = query.count()
        items = query.order_by(Ingredient.name).offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def update_ingredient(
        db: Session,
        ingredient_id: int,
        ingredient: IngredientUpdate
    ) -> Optional[Ingredient]:
        """Update ingredient"""
        db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        if not db_ingredient:
            return None
        
        update_data = ingredient.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ingredient, field, value)
        
        db.commit()
        db.refresh(db_ingredient)
        return db_ingredient
    
    @staticmethod
    def delete_ingredient(db: Session, ingredient_id: int) -> bool:
        """Delete ingredient"""
        db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
        if db_ingredient:
            db.delete(db_ingredient)
            db.commit()
            return True
        return False
    
    # Menu Item Ingredient operations
    
    @staticmethod
    def add_ingredient_to_menu_item(
        db: Session,
        menu_item_id: int,
        ingredient_id: int,
        quantity: Optional[str] = None,
        is_optional: bool = False
    ) -> MenuItemIngredient:
        """Add ingredient to menu item"""
        db_menu_item_ingredient = MenuItemIngredient(
            menu_item_id=menu_item_id,
            ingredient_id=ingredient_id,
            quantity=quantity,
            is_optional=is_optional
        )
        db.add(db_menu_item_ingredient)
        db.commit()
        db.refresh(db_menu_item_ingredient)
        return db_menu_item_ingredient
    
    @staticmethod
    def remove_ingredient_from_menu_item(
        db: Session,
        menu_item_id: int,
        ingredient_id: int
    ) -> bool:
        """Remove ingredient from menu item"""
        db_menu_item_ingredient = db.query(MenuItemIngredient).filter(
            MenuItemIngredient.menu_item_id == menu_item_id,
            MenuItemIngredient.ingredient_id == ingredient_id
        ).first()
        
        if db_menu_item_ingredient:
            db.delete(db_menu_item_ingredient)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_menu_item_ingredients(db: Session, menu_item_id: int) -> List[MenuItemIngredient]:
        """Get all ingredients for a menu item"""
        return db.query(MenuItemIngredient).filter(
            MenuItemIngredient.menu_item_id == menu_item_id
        ).all()
