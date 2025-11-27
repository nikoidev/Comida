"""
Tests for user endpoints
"""
import pytest
from fastapi import status


class TestCreateUser:
    """Test user creation endpoint"""
    
    def test_create_user_success(self, client, test_user_data):
        """Test successful user creation"""
        response = client.post("/api/users/", json=test_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]
        assert "password" not in data  # Password should not be returned
    
    def test_create_user_duplicate_username(self, client, test_user_data):
        """Test creating user with duplicate username"""
        # Create first user
        client.post("/api/users/", json=test_user_data)
        
        # Try to create duplicate
        response = client.post("/api/users/", json=test_user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_user_invalid_email(self, client, test_user_data):
        """Test creating user with invalid email"""
        test_user_data["email"] = "invalid-email"
        response = client.post("/api/users/", json=test_user_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_user_missing_fields(self, client):
        """Test creating user with missing required fields"""
        response = client.post("/api/users/", json={})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetUsers:
    """Test get users list endpoint"""
    
    def test_get_users_empty(self, client):
        """Test getting users when database is empty"""
        response = client.get("/api/users/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0
    
    def test_get_users_with_pagination(self, client, test_user_data):
        """Test getting users with pagination"""
        # Create multiple users
        for i in range(15):
            user_data = test_user_data.copy()
            user_data["username"] = f"user{i}"
            user_data["email"] = f"user{i}@example.com"
            client.post("/api/users/", json=user_data)
        
        # Get first page
        response = client.get("/api/users/?page=1&limit=10")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) == 10
        assert data["total"] == 15
        assert data["page"] == 1
        assert data["pages"] == 2
    
    def test_get_users_with_search(self, client, test_user_data):
        """Test searching users"""
        # Create users
        client.post("/api/users/", json=test_user_data)
        
        # Search by username
        response = client.get(f"/api/users/?search={test_user_data['username']}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) >= 1
        assert data["items"][0]["username"] == test_user_data["username"]


class TestGetUser:
    """Test get single user endpoint"""
    
    def test_get_user_success(self, client, test_user_data):
        """Test getting a single user by ID"""
        # Create user
        create_response = client.post("/api/users/", json=test_user_data)
        user_id = create_response.json()["id"]
        
        # Get user
        response = client.get(f"/api/users/{user_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == test_user_data["username"]
    
    def test_get_user_not_found(self, client):
        """Test getting non-existent user"""
        response = client.get("/api/users/99999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateUser:
    """Test update user endpoint"""
    
    def test_update_user_success(self, client, test_user_data):
        """Test successful user update"""
        # Create user
        create_response = client.post("/api/users/", json=test_user_data)
        user_id = create_response.json()["id"]
        
        # Update user
        update_data = {
            "first_name": "Updated",
            "last_name": "Name"
        }
        response = client.put(f"/api/users/{user_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["first_name"] == "Updated"
        assert data["last_name"] == "Name"
    
    def test_update_user_not_found(self, client):
        """Test updating non-existent user"""
        update_data = {"first_name": "Test"}
        response = client.put("/api/users/99999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteUser:
    """Test delete user endpoint"""
    
    def test_delete_user_success(self, client, test_user_data):
        """Test successful user deletion"""
        # Create user
        create_response = client.post("/api/users/", json=test_user_data)
        user_id = create_response.json()["id"]
        
        # Delete user
        response = client.delete(f"/api/users/{user_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify user is deleted
        get_response = client.get(f"/api/users/{user_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_user_not_found(self, client):
        """Test deleting non-existent user"""
        response = client.delete("/api/users/99999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
