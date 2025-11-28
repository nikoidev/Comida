from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantResponse
from ...services.restaurant_service import RestaurantService
from ..deps import get_current_active_user
from ...models.user import User

router = APIRouter()


@router.post("/", response_model=RestaurantResponse, status_code=status.HTTP_201_CREATED)
def create_restaurant(
    restaurant: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new restaurant"""
    return RestaurantService.create_restaurant(db, restaurant, current_user.id)


@router.get("/my-restaurants", response_model=List[RestaurantResponse])
def get_my_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all restaurants owned by current user"""
    return RestaurantService.get_user_restaurants(db, current_user.id)


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get restaurant by ID"""
    restaurant = RestaurantService.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Check ownership
    if not RestaurantService.check_ownership(restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized to access this restaurant")
    
    return restaurant


@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
    restaurant_id: int,
    restaurant: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update restaurant"""
    db_restaurant = RestaurantService.get_restaurant(db, restaurant_id)
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Check ownership
    if not RestaurantService.check_ownership(db_restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized to modify this restaurant")
    
    return RestaurantService.update_restaurant(db, restaurant_id, restaurant)


@router.post("/{restaurant_id}/publish", response_model=RestaurantResponse)
def publish_restaurant(
    restaurant_id: int,
    is_published: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Publish or unpublish restaurant"""
    db_restaurant = RestaurantService.get_restaurant(db, restaurant_id)
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Check ownership
    if not RestaurantService.check_ownership(db_restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized to publish this restaurant")
    
    return RestaurantService.publish_restaurant(db, restaurant_id, is_published)


@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete restaurant"""
    db_restaurant = RestaurantService.get_restaurant(db, restaurant_id)
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Check ownership
    if not RestaurantService.check_ownership(db_restaurant, current_user.id, current_user.is_superuser):
        raise HTTPException(status_code=403, detail="Not authorized to delete this restaurant")
    
    RestaurantService.delete_restaurant(db, restaurant_id)
    return None


# Public endpoint (no auth required)
@router.get("/public/{slug}", response_model=RestaurantResponse)
def get_restaurant_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get published restaurant by slug (public endpoint)"""
    restaurant = RestaurantService.get_restaurant_by_slug(db, slug)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant
