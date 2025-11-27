"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.models import User, Role, Permission
from app.core.security import get_password_hash

# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Create admin permission
    admin_permission = Permission(
        name="Admin Permission",
        code="admin.all",
        resource="all",
        action="all"
    )
    db.add(admin_permission)
    db.commit()
    
    # Create admin role with permission
    admin_role = Role(
        name="Admin",
        description="Administrator role",
        permissions=[admin_permission]
    )
    db.add(admin_role)
    db.commit()
    
    # Create admin user
    admin_user = User(
        username="testadmin",
        email="testadmin@example.com",
        hashed_password=get_password_hash("testpass123"),
        first_name="Test",
        last_name="Admin",
        is_active=True,
        is_superuser=True,
        roles=[admin_role]
    )
    db.add(admin_user)
    db.commit()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client with authentication"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        # Login to get token
        login_response = test_client.post(
            "/api/auth/login",
            data={"username": "testadmin", "password": "testpass123"}
        )
        token = login_response.json()["access_token"]
        
        # Add token to all requests
        test_client.headers = {"Authorization": f"Bearer {token}"}
        
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User"
    }


@pytest.fixture
def test_role_data():
    """Sample role data for testing"""
    return {
        "name": "Test Role",
        "description": "A test role"
    }


@pytest.fixture
def test_permission_data():
    """Sample permission data for testing"""
    return {
        "name": "Test Permission",
        "code": "test.permission",
        "resource": "test",
        "action": "read"
    }
