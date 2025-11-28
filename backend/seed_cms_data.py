"""
Seed data script for CMS
Creates sample restaurant, categories, menu items, and ingredients for testing
"""
from app.core.database import SessionLocal
from app.models import Restaurant, Category, MenuItem, Ingredient, MenuItemIngredient, User
from app.core.security import get_password_hash
from decimal import Decimal

def seed_cms_data():
    """Create sample data for testing"""
    db = SessionLocal()
    
    try:
        print("🌱 Seeding CMS data...")
        
        # Check if admin user exists, if not create one
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            print("Creating admin user...")
            admin_user = User(
                username="admin",
                email="admin@comida.com",
                hashed_password=get_password_hash("admin123"),
                first_name="Admin",
                last_name="User",
                is_active=True,
                is_superuser=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print("✅ Admin user created")
        
        # Create sample restaurant
        print("\nCreating sample restaurant...")
        restaurant = Restaurant(
            user_id=admin_user.id,
            name="Pizzería Don Luigi",
            slug="pizzeria-don-luigi",
            description="Auténtica pizza italiana desde 1995. Recetas tradicionales con ingredientes frescos.",
            phone="+1234567890",
            whatsapp="+1234567890",
            email="info@donluigi.com",
            address="Calle Principal 123",
            city="Ciudad de México",
            country="México",
            opening_hours={
                "monday": "11:00-22:00",
                "tuesday": "11:00-22:00",
                "wednesday": "11:00-22:00",
                "thursday": "11:00-22:00",
                "friday": "11:00-23:00",
                "saturday": "12:00-23:00",
                "sunday": "12:00-22:00"
            },
            primary_color="#DC143C",
            secondary_color="#228B22",
            meta_title="Pizzería Don Luigi - Auténtica Pizza Italiana",
            meta_description="Las mejores pizzas italianas en Ciudad de México. Ingredientes frescos y recetas tradicionales.",
            is_published=True
        )
        db.add(restaurant)
        db.commit()
        db.refresh(restaurant)
        print(f"✅ Restaurant created: {restaurant.name}")
        
        # Create categories
        print("\nCreating categories...")
        categories_data = [
            {"name": "Pizzas", "icon": "🍕", "order": 1},
            {"name": "Bebidas", "icon": "🥤", "order": 2},
            {"name": "Postres", "icon": "🍰", "order": 3},
            {"name": "Entradas", "icon": "🥗", "order": 4}
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = Category(
                restaurant_id=restaurant.id,
                name=cat_data["name"],
                slug=cat_data["name"].lower(),
                icon=cat_data["icon"],
                order=cat_data["order"],
                is_active=True
            )
            db.add(category)
            db.commit()
            db.refresh(category)
            categories[cat_data["name"]] = category
            print(f"  ✅ {cat_data['icon']} {cat_data['name']}")
        
        # Create common ingredients
        print("\nCreating ingredients...")
        ingredients_data = [
            {"name": "Mozzarella", "icon": "🧀", "is_allergen": True},
            {"name": "Tomate", "icon": "🍅", "is_allergen": False},
            {"name": "Albahaca", "icon": "🌿", "is_allergen": False},
            {"name": "Pepperoni", "icon": "🥓", "is_allergen": False},
            {"name": "Champiñones", "icon": "🍄", "is_allergen": False},
            {"name": "Aceitunas", "icon": "🫒", "is_allergen": False},
            {"name": "Piña", "icon": "🍍", "is_allergen": False},
            {"name": "Jamón", "icon": "🥩", "is_allergen": False},
        ]
        
        ingredients = {}
        for ing_data in ingredients_data:
            ingredient = Ingredient(**ing_data)
            db.add(ingredient)
            db.commit()
            db.refresh(ingredient)
            ingredients[ing_data["name"]] = ingredient
            print(f"  ✅ {ing_data['icon']} {ing_data['name']}")
        
        # Create menu items (pizzas)
        print("\nCreating menu items...")
        pizzas_data = [
            {
                "name": "Pizza Margarita",
                "description": "Clásica pizza italiana con mozzarella fresca, tomate y albahaca",
                "price": Decimal("12.99"),
                "preparation_time": 25,
                "serves": 2,
                "is_vegetarian": True,
                "ingredients": ["Mozzarella", "Tomate", "Albahaca"]
            },
            {
                "name": "Pizza Pepperoni",
                "description": "Pizza con abundante pepperoni y queso mozzarella",
                "price": Decimal("14.99"),
                "preparation_time": 25,
                "serves": 2,
                "is_spicy": True,
                "spicy_level": 2,
                "ingredients": ["Mozzarella", "Tomate", "Pepperoni"]
            },
            {
                "name": "Pizza Hawaiana",
                "description": "Combinación única de jamón y piña sobre queso mozzarella",
                "price": Decimal("13.99"),
                "preparation_time": 25,
                "serves": 2,
                "ingredients": ["Mozzarella", "Tomate", "Jamón", "Piña"]
            },
            {
                "name": "Pizza Vegetariana",
                "description": "Deliciosa mezcla de vegetales frescos",
                "price": Decimal("13.49"),
                "preparation_time": 30,
                "serves": 2,
                "is_vegetarian": True,
                "ingredients": ["Mozzarella", "Tomate", "Champiñones", "Aceitunas"]
            }
        ]
        
        for idx, pizza_data in enumerate(pizzas_data):
            ingredient_names = pizza_data.pop("ingredients")
            
            menu_item = MenuItem(
                restaurant_id=restaurant.id,
                category_id=categories["Pizzas"].id,
                slug=pizza_data["name"].lower().replace(" ", "-"),
                currency="USD",
                is_available=True,
                is_featured=(pizza_data["name"] == "Pizza Margarita"),
                order=idx,
                **pizza_data
            )
            db.add(menu_item)
            db.commit()
            db.refresh(menu_item)
            
            # Add ingredients to menu item
            for ing_name in ingredient_names:
                menu_item_ingredient = MenuItemIngredient(
                    menu_item_id=menu_item.id,
                    ingredient_id=ingredients[ing_name].id
                )
                db.add(menu_item_ingredient)
            
            db.commit()
            print(f"  ✅ {menu_item.name} - ${menu_item.price}")
        
        # Create some beverages
        beverages_data = [
            {"name": "Coca-Cola", "price": Decimal("2.50")},
            {"name": "Agua Mineral", "price": Decimal("1.50")},
            {"name": "Limonada Natural", "price": Decimal("3.00")}
        ]
        
        for idx, bev_data in enumerate(beverages_data):
            menu_item = MenuItem(
                restaurant_id=restaurant.id,
                category_id=categories["Bebidas"].id,
                slug=bev_data["name"].lower().replace(" ", "-"),
                description=f"Refrescante {bev_data['name']}",
                price=bev_data["price"],
                currency="USD",
                is_available=True,
                order=idx
            )
            db.add(menu_item)
            db.commit()
            print(f"  ✅ {menu_item.name} - ${menu_item.price}")
        
        print("\n✅ Seed data created successfully!")
        print(f"\n📊 Summary:")
        print(f"  - Restaurant: {restaurant.name}")
        print(f"  - Categories: {len(categories)}")
        print(f"  - Ingredients: {len(ingredients)}")
        print(f"  - Menu Items: {len(pizzas_data) + len(beverages_data)}")
        print(f"\n🌐 Access your restaurant at: /api/restaurants/public/{restaurant.slug}")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_cms_data()
