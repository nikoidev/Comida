from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ...core.database import get_db
from ...schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse, CategoryListResponse
from ...services.category_service import CategoryService
from ...services.restaurant_service import RestaurantService
from ..deps import get_current_active_user
from ...models.user import User

router = APIRouter()


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new category"""
    # Check restaurant ownership
    restaurant = RestaurantService.get_restaurant(db, category.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return CategoryService.create_category(db, category)


@router.get("/restaurant/{restaurant_id}", response_model=CategoryListResponse)
def get_restaurant_categories(
    restaurant_id: int,
    active_only: bool = Query(False, description="Show only active categories"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all categories for a restaurant"""
    # Check restaurant ownership
    restaurant = RestaurantService.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    categories = CategoryService.get_restaurant_categories(db, restaurant_id, active_only)
    return CategoryListResponse(items=categories, total=len(categories))


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get category by ID"""
    category = CategoryService.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check restaurant ownership
    restaurant = RestaurantService.get_restaurant(db, category.restaurant_id)
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update category"""
    db_category = CategoryService.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check restaurant ownership
    restaurant = RestaurantService.get_restaurant(db, db_category.restaurant_id)
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return CategoryService.update_category(db, category_id, category)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete category"""
    db_category = CategoryService.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check restaurant ownership
    restaurant = RestaurantService.get_restaurant(db, db_category.restaurant_id)
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    CategoryService.delete_category(db, category_id)
    return None


@router.post("/reorder", status_code=status.HTTP_200_OK)
def reorder_categories(
    category_orders: List[dict],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Reorder categories - expects list of {id: int, order: int}"""
    # Verify ownership of first category (assume all belong to same restaurant)
    if category_orders:
        first_category = CategoryService.get_category(db, category_orders[0]['id'])
        if first_category:
            restaurant = RestaurantService.get_restaurant(db, first_category.restaurant_id)
            if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
                raise HTTPException(status_code=403, detail="Not authorized")
    
    success = CategoryService.reorder_categories(db, category_orders)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to reorder categories")
    
    return {"message": "Categories reordered successfully"}
