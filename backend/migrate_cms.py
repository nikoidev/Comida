"""
Database migration script for CMS tables
Run this script to create the new CMS tables in the database
"""
from app.core.database import engine, Base
from app.models import Restaurant, Category, MenuItem, Ingredient, MenuItemIngredient

def create_cms_tables():
    """Create all CMS tables"""
    print("Creating CMS tables...")
    
    # This will create all tables defined in Base.metadata
    # It will skip tables that already exist
    Base.metadata.create_all(bind=engine)
    
    print("✅ CMS tables created successfully!")
    print("\nNew tables:")
    print("  - restaurants")
    print("  - categories")
    print("  - menu_items")
    print("  - ingredients")
    print("  - menu_item_ingredients")

if __name__ == "__main__":
    create_cms_tables()
