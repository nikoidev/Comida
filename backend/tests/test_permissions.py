"""
Tests for permission endpoints
"""
import pytest
from fastapi import status


class TestCreatePermission:
    """Test permission creation endpoint"""
    
    def test_create_permission_success(self, client):
        """Test successful permission creation"""
        permission_data = {
            "name": "Create Users",
            "code": "users.create",
            "description": "Permission to create users",
            "resource": "users",
            "action": "create"
        }
        response = client.post("/api/permissions/", json=permission_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == permission_data["name"]
        assert data["code"] == permission_data["code"]
    
    def test_create_permission_duplicate_code(self, client):
        """Test creating permission with duplicate code"""
        permission_data = {
            "name": "Test Permission",
            "code": "test.permission",
            "resource": "test",
            "action": "create"
        }
        # Create first permission
        client.post("/api/permissions/", json=permission_data)
        
        # Try to create duplicate
        response = client.post("/api/permissions/", json=permission_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestGetPermissions:
    """Test get permissions list endpoint"""
    
    def test_get_permissions_empty(self, client):
        """Test getting permissions when database is empty"""
        response = client.get("/api/permissions/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data["items"], list)
    
    def test_get_permissions_with_pagination(self, client):
        """Test getting permissions with pagination"""
        # Create multiple permissions
        for i in range(15):
            permission_data = {
                "name": f"Permission {i}",
                "code": f"test.permission{i}",
                "resource": "test",
                "action": "read"
            }
            client.post("/api/permissions/", json=permission_data)
        
        # Get first page
        response = client.get("/api/permissions/?page=1&limit=10")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 10
        assert data["total"] == 15
    
    def test_get_permissions_filter_by_resource(self, client):
        """Test filtering permissions by resource"""
        # Create permissions with different resources
        client.post("/api/permissions/", json={
            "name": "User Permission",
            "code": "users.read",
            "resource": "users",
            "action": "read"
        })
        client.post("/api/permissions/", json={
            "name": "Role Permission",
            "code": "roles.read",
            "resource": "roles",
            "action": "read"
        })
        
        # Filter by resource
        response = client.get("/api/permissions/?resource=users")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(perm["resource"] == "users" for perm in data["items"])
    
    def test_get_permissions_filter_by_action(self, client):
        """Test filtering permissions by action"""
        # Create permissions with different actions
        client.post("/api/permissions/", json={
            "name": "Create",
            "code": "test.create",
            "resource": "test",
            "action": "create"
        })
        client.post("/api/permissions/", json={
            "name": "Read",
            "code": "test.read",
            "resource": "test",
            "action": "read"
        })
        
        # Filter by action
        response = client.get("/api/permissions/?action=create")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(perm["action"] == "create" for perm in data["items"])


class TestGetPermission:
    """Test get single permission endpoint"""
    
    def test_get_permission_success(self, client):
        """Test getting a single permission by ID"""
        # Create permission
        permission_data = {
            "name": "Test",
            "code": "test.read",
            "resource": "test",
            "action": "read"
        }
        create_response = client.post("/api/permissions/", json=permission_data)
        permission_id = create_response.json()["id"]
        
        # Get permission
        response = client.get(f"/api/permissions/{permission_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == permission_id
    
    def test_get_permission_not_found(self, client):
        """Test getting non-existent permission"""
        response = client.get("/api/permissions/99999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdatePermission:
    """Test update permission endpoint"""
    
    def test_update_permission_success(self, client):
        """Test successful permission update"""
        # Create permission
        permission_data = {
            "name": "Original",
            "code": "test.original",
            "resource": "test",
            "action": "read"
        }
        create_response = client.post("/api/permissions/", json=permission_data)
        permission_id = create_response.json()["id"]
        
        # Update permission
        update_data = {
            "name": "Updated",
            "description": "Updated description"
        }
        response = client.put(f"/api/permissions/{permission_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated"


class TestDeletePermission:
    """Test delete permission endpoint"""
    
    def test_delete_permission_success(self, client):
        """Test successful permission deletion"""
        # Create permission
        permission_data = {
            "name": "To Delete",
            "code": "test.delete",
            "resource": "test",
            "action": "delete"
        }
        create_response = client.post("/api/permissions/", json=permission_data)
        permission_id = create_response.json()["id"]
        
        # Delete permission
        response = client.delete(f"/api/permissions/{permission_id}")
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify permission is deleted
        get_response = client.get(f"/api/permissions/{permission_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
