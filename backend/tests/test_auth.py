"""
Tests for authentication endpoints
"""
import pytest
from fastapi import status


class TestLogin:
    """Test login endpoint"""
    
    def test_login_success(self, client, db, test_user_data):
        """Test successful login"""
        # First create the user
        response = client.post("/api/users/", json=test_user_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Now login
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        login_data = {
            "username": "nonexistent",
            "password": "wrongpassword"
        }
        response = client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields"""
        response = client.post("/api/auth/login", data={})
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestRefreshToken:
    """Test refresh token endpoint"""
    
    def test_refresh_token_success(self, client, db, test_user_data):
        """Test successful token refresh"""
        # Create user and login
        client.post("/api/users/", json=test_user_data)
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        login_response = client.post("/api/auth/login", data=login_data)
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh token
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
    
    def test_refresh_token_invalid(self, client):
        """Test refresh with invalid token"""
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": "invalid_token"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetCurrentUser:
    """Test get current user endpoint"""
    
    def test_get_current_user_success(self, client, db, test_user_data):
        """Test getting current user with valid token"""
        # Create user and login
        client.post("/api/users/", json=test_user_data)
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        login_response = client.post("/api/auth/login", data=login_data)
        access_token = login_response.json()["access_token"]
        
        # Get current user
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]
    
    def test_get_current_user_no_token(self, client):
        """Test getting current user without token"""
        response = client.get("/api/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestChangePassword:
    """Test change password endpoint"""
    
    def test_change_password_success(self, client, db, test_user_data):
        """Test successful password change"""
        # Create user and login
        client.post("/api/users/", json=test_user_data)
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        login_response = client.post("/api/auth/login", data=login_data)
        access_token = login_response.json()["access_token"]
        
        # Change password
        headers = {"Authorization": f"Bearer {access_token}"}
        new_password_data = {
            "current_password": test_user_data["password"],
            "new_password": "NewPass123!"
        }
        response = client.post(
            "/api/auth/change-password",
            json=new_password_data,
            headers=headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify can login with new password
        login_data["password"] = "NewPass123!"
        response = client.post("/api/auth/login", data=login_data)
        assert response.status_code == status.HTTP_200_OK
    
    def test_change_password_wrong_current(self, client, db, test_user_data):
        """Test password change with wrong current password"""
        # Create user and login
        client.post("/api/users/", json=test_user_data)
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        login_response = client.post("/api/auth/login", data=login_data)
        access_token = login_response.json()["access_token"]
        
        # Try to change with wrong current password
        headers = {"Authorization": f"Bearer {access_token}"}
        new_password_data = {
            "current_password": "WrongPassword123!",
            "new_password": "NewPass123!"
        }
        response = client.post(
            "/api/auth/change-password",
            json=new_password_data,
            headers=headers
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestLogout:
    """Test logout endpoint"""
    
    def test_logout_success(self, client, db, test_user_data):
        """Test successful logout"""
        # Create user and login
        client.post("/api/users/", json=test_user_data)
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        login_response = client.post("/api/auth/login", data=login_data)
        access_token = login_response.json()["access_token"]
        
        # Logout
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/api/auth/logout", headers=headers)
        
        assert response.status_code == status.HTTP_200_OK
