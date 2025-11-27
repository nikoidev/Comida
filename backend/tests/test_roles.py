"""
Tests for role endpoints
"""
import pytest
from fastapi import status


class TestCreateRole:
    """Test role creation endpoint"""
    
    def test_create_role_success(self, client):
        """Test successful role creation"""
        role_data = {
            "name": "Test Role",
            "description": "A test role",
            "is_active": True
        }
        response = client.post("/api/roles/", json=role_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == role_data["name"]
        assert data["description"] == role_data["description"]
    
    def test_create_role_duplicate_name(self, client):
        """Test creating role with duplicate name"""
        role_data = {
            "name": "Duplicate Role",
            "description": "Test"
        }
        # Create first role
        client.post("/api/roles/", json=role_data)
        
        # Try to create duplicate
        response = client.post("/api/roles/", json=role_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestGetRoles:
    """Test get roles list endpoint"""
    
    def test_get_roles_empty(self, client):
        """Test getting roles when database is empty"""
        response = client.get("/api/roles/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data["items"], list)
    
    def test_get_roles_with_pagination(self, client):
        """Test getting roles with pagination"""
        # Create multiple roles
        for i in range(15):
            role_data = {
                "name": f"Role {i}",
                "description": f"Description {i}"
            }
            client.post("/api/roles/", json=role_data)
        
        # Get first page
        response = client.get("/api/roles/?page=1&limit=10")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 10
        assert data["total"] == 16  # 15 created + 1 admin
    
    def test_get_roles_with_filter(self, client):
        """Test filtering roles by active status"""
        # Create active and inactive roles
        client.post("/api/roles/", json={"name": "Active", "is_active": True})
        client.post("/api/roles/", json={"name": "Inactive", "is_active": False})
        
        # Filter by active
        response = client.get("/api/roles/?is_active=true")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(role["is_active"] for role in data["items"])


class TestGetRole:
    """Test get single role endpoint"""
    
    def test_get_role_success(self, client):
        """Test getting a single role by ID"""
        # Create role
        role_data = {"name": "Test Role", "description": "Test"}
        create_response = client.post("/api/roles/", json=role_data)
        role_id = create_response.json()["id"]
        
        # Get role
        response = client.get(f"/api/roles/{role_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == role_id
        assert data["name"] == role_data["name"]
    
    def test_get_role_not_found(self, client):
        """Test getting non-existent role"""
        response = client.get("/api/roles/99999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateRole:
    """Test update role endpoint"""
    
    def test_update_role_success(self, client):
        """Test successful role update"""
        # Create role
        role_data = {"name": "Original", "description": "Original description"}
        create_response = client.post("/api/roles/", json=role_data)
        role_id = create_response.json()["id"]
        
        # Update role
        update_data = {
            "name": "Updated",
            "description": "Updated description"
        }
        response = client.put(f"/api/roles/{role_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated"
        assert data["description"] == "Updated description"


class TestDeleteRole:
    """Test delete role endpoint"""
    
    def test_delete_role_success(self, client):
        """Test successful role deletion"""
        # Create role
        role_data = {"name": "To Delete", "description": "Test"}
        create_response = client.post("/api/roles/", json=role_data)
        role_id = create_response.json()["id"]
        
        # Delete role
        response = client.delete(f"/api/roles/{role_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify role is deleted
        get_response = client.get(f"/api/roles/{role_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
