# Testing Guide

## Backend Testing

### Setup

1. Install test dependencies:
```bash
cd backend
pipenv install --dev
```

2. Run all tests:
```bash
pipenv run pytest
```

3. Run tests with coverage:
```bash
pipenv run pytest --cov=app --cov-report=html
```

4. Run specific test file:
```bash
pipenv run pytest tests/test_auth.py
```

5. Run specific test class or function:
```bash
pipenv run pytest tests/test_auth.py::TestLogin::test_login_success
```

### Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_auth.py         # Authentication tests
├── test_users.py        # User CRUD tests
├── test_roles.py        # Role CRUD tests
└── test_permissions.py  # Permission CRUD tests
```

### Writing Tests

Example test:
```python
def test_create_user_success(client, test_user_data):
    """Test successful user creation"""
    response = client.post("/api/users/", json=test_user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == test_user_data["username"]
```

### Coverage Reports

After running tests with coverage, open the HTML report:
```bash
# Windows
start backend/htmlcov/index.html

# Linux/Mac
open backend/htmlcov/index.html
```

## Frontend Testing

### Setup (Future)

```bash
cd frontend
npm install --save-dev @testing-library/react @testing-library/jest-dom jest
```

### Running Tests

```bash
npm test
```

## CI/CD

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

### GitHub Actions Workflow

See `.github/workflows/ci.yml` for the complete CI/CD pipeline.

## Best Practices

1. **Write descriptive test names** - Use `test_<action>_<expected_result>`
2. **Use fixtures** - Reuse common setup code
3. **Test edge cases** - Not just happy paths
4. **Keep tests isolated** - Each test should be independent
5. **Mock external dependencies** - Don't rely on external services
6. **Aim for high coverage** - Target 80%+ code coverage

## Debugging Tests

Run tests in verbose mode:
```bash
pipenv run pytest -v
```

Run tests with print statements:
```bash
pipenv run pytest -s
```

Run tests and stop at first failure:
```bash
pipenv run pytest -x
```
