from app.core.database import SessionLocal, engine, Base
from app.models import User, Role, Permission
from app.core.security import get_password_hash


def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            print("Database already initialized")
            return
        
        # Create default permissions
        permissions_data = [
            {"name": "Crear Usuario", "code": "user.create", "resource": "users", "action": "create"},
            {"name": "Leer Usuario", "code": "user.read", "resource": "users", "action": "read"},
            {"name": "Actualizar Usuario", "code": "user.update", "resource": "users", "action": "update"},
            {"name": "Eliminar Usuario", "code": "user.delete", "resource": "users", "action": "delete"},
            {"name": "Crear Rol", "code": "role.create", "resource": "roles", "action": "create"},
            {"name": "Leer Rol", "code": "role.read", "resource": "roles", "action": "read"},
            {"name": "Actualizar Rol", "code": "role.update", "resource": "roles", "action": "update"},
            {"name": "Eliminar Rol", "code": "role.delete", "resource": "roles", "action": "delete"},
            {"name": "Crear Permiso", "code": "permission.create", "resource": "permissions", "action": "create"},
            {"name": "Leer Permiso", "code": "permission.read", "resource": "permissions", "action": "read"},
            {"name": "Actualizar Permiso", "code": "permission.update", "resource": "permissions", "action": "update"},
            {"name": "Eliminar Permiso", "code": "permission.delete", "resource": "permissions", "action": "delete"},
        ]
        
        permissions = []
        for perm_data in permissions_data:
            permission = Permission(**perm_data)
            db.add(permission)
            permissions.append(permission)
        
        db.commit()
        
        # Create admin role with all permissions
        admin_role = Role(
            name="Administrador",
            description="Administrador con acceso completo",
            permissions=permissions
        )
        db.add(admin_role)
        
        # Create user role with read permissions
        user_permissions = [p for p in permissions if p.action == "read"]
        user_role = Role(
            name="Usuario",
            description="Usuario regular con acceso de lectura",
            permissions=user_permissions
        )
        db.add(user_role)
        
        db.commit()
        
        # Create admin user
        admin_user = User(
            email="admin@example.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            is_active=True,
            is_superuser=True,
            roles=[admin_role]
        )
        db.add(admin_user)
        
        # Create regular user
        regular_user = User(
            email="user@example.com",
            username="user",
            hashed_password=get_password_hash("user123"),
            first_name="Regular",
            last_name="User",
            is_active=True,
            is_superuser=False,
            roles=[user_role]
        )
        db.add(regular_user)
        
        db.commit()
        
        print("Database initialized successfully!")
        print("Admin user created: username='admin', password='admin123'")
        print("Regular user created: username='user', password='user123'")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
