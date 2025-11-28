from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from ...core.database import get_db
from ...schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemResponse, MenuItemListResponse
from ...services.menu_item_service import MenuItemService
from ...services.restaurant_service import RestaurantService
from ..deps import get_current_active_user
from ...models.user import User

router = APIRouter()


@router.post("/", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_menu_item(
    menu_item: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new menu item"""
    # Check restaurant ownership
    restaurant = RestaurantService.get_restaurant(db, menu_item.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return MenuItemService.create_menu_item(db, menu_item)


@router.get("/restaurant/{restaurant_id}", response_model=MenuItemListResponse)
def get_restaurant_menu_items(
    restaurant_id: int,
    category_id: Optional[int] = Query(None, description="Filter by category"),
    available_only: bool = Query(False, description="Show only available items"),
    featured_only: bool = Query(False, description="Show only featured items"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all menu items for a restaurant"""
    # Check restaurant ownership
    restaurant = RestaurantService.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    skip = (page - 1) * limit
    items, total = MenuItemService.get_restaurant_menu_items(
        db, restaurant_id, category_id, available_only, featured_only, skip, limit
    )
    
    pages = (total + limit - 1) // limit
    return MenuItemListResponse(items=items, total=total, page=page, pages=pages)


@router.get("/{menu_item_id}", response_model=MenuItemResponse)
def get_menu_item(
    menu_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get menu item by ID"""
    menu_item = MenuItemService.get_menu_item(db, menu_item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Check restaurant ownership
    restaurant = RestaurantService.get_restaurant(db, menu_item.restaurant_id)
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return menu_item


@router.put("/{menu_item_id}", response_model=MenuItemResponse)
def update_menu_item(
    menu_item_id: int,
    menu_item: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update menu item"""
    db_menu_item = MenuItemService.get_menu_item(db, menu_item_id)
    if not db_menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Check restaurant ownership
    restaurant = RestaurantService.get_restaurant(db, db_menu_item.restaurant_id)
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return MenuItemService.update_menu_item(db, menu_item_id, menu_item)


@router.delete("/{menu_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(
    menu_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete menu item"""
    db_menu_item = MenuItemService.get_menu_item(db, menu_item_id)
    if not db_menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Check restaurant ownership
    restaurant = RestaurantService.get_restaurant(db, db_menu_item.restaurant_id)
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    MenuItemService.delete_menu_item(db, menu_item_id)
    return None


@router.post("/{menu_item_id}/toggle-availability", response_model=MenuItemResponse)
def toggle_availability(
    menu_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Toggle menu item availability"""
    db_menu_item = MenuItemService.get_menu_item(db, menu_item_id)
    if not db_menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Check restaurant ownership
    restaurant = RestaurantService.get_restaurant(db, db_menu_item.restaurant_id)
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return MenuItemService.toggle_availability(db, menu_item_id)


@router.post("/{menu_item_id}/toggle-featured", response_model=MenuItemResponse)
def toggle_featured(
    menu_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Toggle menu item featured status"""
    db_menu_item = MenuItemService.get_menu_item(db, menu_item_id)
    if not db_menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Check restaurant ownership
    restaurant = RestaurantService.get_restaurant(db, db_menu_item.restaurant_id)
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return MenuItemService.toggle_featured(db, menu_item_id)
