from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from ...core.database import get_db
from ...schemas.ingredient import (
    IngredientCreate, IngredientUpdate, IngredientResponse, IngredientListResponse,
    MenuItemIngredientCreate
)
from ...services.ingredient_service import IngredientService
from ...services.menu_item_service import MenuItemService
from ...services.restaurant_service import RestaurantService
from ..deps import get_current_active_user
from ...models.user import User

router = APIRouter()


@router.post("/", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
def create_ingredient(
    ingredient: IngredientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new ingredient"""
    # Check if ingredient already exists
    existing = IngredientService.get_ingredient_by_name(db, ingredient.name)
    if existing:
        raise HTTPException(status_code=400, detail="Ingredient already exists")
    
    return IngredientService.create_ingredient(db, ingredient)


@router.get("/", response_model=IngredientListResponse)
def get_all_ingredients(
    allergens_only: bool = Query(False, description="Show only allergens"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=200, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all ingredients"""
    skip = (page - 1) * limit
    items, total = IngredientService.get_all_ingredients(db, allergens_only, skip, limit)
    return IngredientListResponse(items=items, total=total)


@router.get("/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get ingredient by ID"""
    ingredient = IngredientService.get_ingredient(db, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@router.put("/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(
    ingredient_id: int,
    ingredient: IngredientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update ingredient"""
    updated = IngredientService.update_ingredient(db, ingredient_id, ingredient)
    if not updated:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return updated


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete ingredient"""
    success = IngredientService.delete_ingredient(db, ingredient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return None


# Menu Item Ingredient endpoints

@router.post("/menu-item/{menu_item_id}/add", status_code=status.HTTP_201_CREATED)
def add_ingredient_to_menu_item(
    menu_item_id: int,
    ingredient_data: MenuItemIngredientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Add ingredient to menu item"""
    # Check menu item exists and user has access
    menu_item = MenuItemService.get_menu_item(db, menu_item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    restaurant = RestaurantService.get_restaurant(db, menu_item.restaurant_id)
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check ingredient exists
    ingredient = IngredientService.get_ingredient(db, ingredient_data.ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    return IngredientService.add_ingredient_to_menu_item(
        db, menu_item_id, ingredient_data.ingredient_id,
        ingredient_data.quantity, ingredient_data.is_optional
    )


@router.delete("/menu-item/{menu_item_id}/remove/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_ingredient_from_menu_item(
    menu_item_id: int,
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Remove ingredient from menu item"""
    # Check menu item exists and user has access
    menu_item = MenuItemService.get_menu_item(db, menu_item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    restaurant = RestaurantService.get_restaurant(db, menu_item.restaurant_id)
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    success = IngredientService.remove_ingredient_from_menu_item(db, menu_item_id, ingredient_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ingredient not found in menu item")
    return None
