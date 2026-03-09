---
name: backend
description: Builds and maintains FastAPI Python backend applications following modern best practices
argument-hint: API endpoints, business logic, database operations, tests, or backend architecture tasks
tools: ['vscode', 'execute', 'read', 'agent', 'edit', 'search', 'web', 'todo']
---

# Backend Agent Guidelines

## Framework & Dependencies

- **Web Framework**: FastAPI for all API endpoints
- **Python Version**: Python 3.12+
- **Testing Framework**: pytest for all tests
- **Environment Configuration**: python-dotenv for loading environment variables
- **Package Management**: pyproject.toml for dependency management
- **ASGI Server**: Uvicorn for running FastAPI applications
- **Database ORM**: SQLAlchemy (if using databases)
- **Validation**: Pydantic models (built into FastAPI)

## Code Style & Conventions

### Naming Conventions
- **Functions/Variables**: snake_case (e.g., `read_item`, `get_user_by_id`, `api_key`)
- **Files/Modules**: snake_case (e.g., `api.py`, `util.py`, `database.py`)
- **Classes**: PascalCase (e.g., `UserService`, `DatabaseConnection`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`, `MAX_CONNECTIONS`)
- **Private**: Prefix with underscore (e.g., `_internal_helper`)

### Type Hints
- Use type hints for all function parameters and return values
- Use modern Python 3.10+ syntax: `str | None` instead of `Optional[str]`
- Use `list[str]` instead of `List[str]`, `dict[str, int]` instead of `Dict[str, int]`
- Examples:
  ```python
  def read_item(item_id: int, q: str | None = None) -> dict[str, Any]:
      pass
  
  def get_users(limit: int = 10) -> list[User]:
      pass
  ```

### Documentation
- Include docstrings for all public functions and classes
- Use Google-style docstrings
- Document parameters, return values, and exceptions
- Examples:
  ```python
  def divide(a: float, b: float) -> float:
      """Return the quotient of a divided by b.

      Args:
          a: The dividend.
          b: The divisor.

      Returns:
          The quotient of a divided by b.

      Raises:
          ValueError: If b is zero.
      """
      if b == 0:
          raise ValueError("Cannot divide by zero")
      return a / b
  ```

### Code Organization
- **api.py**: FastAPI routes and endpoint handlers
- **models.py**: Pydantic models for request/response validation
- **services.py**: Business logic layer
- **database.py**: Database connection and queries
- **util.py**: Utility functions and helpers
- **config.py**: Configuration and settings
- **main.py**: Application entry point
- Maintain flat structure for simple projects; use packages for larger projects

## FastAPI Best Practices

### Application Structure
```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0"
)

# Always include health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}
```

### Endpoint Design
- Use RESTful conventions and HTTP methods correctly:
  - `GET` for reading data
  - `POST` for creating resources
  - `PUT/PATCH` for updating resources
  - `DELETE` for removing resources
- Use path parameters for resource IDs: `@app.get("/items/{item_id}")`
- Use query parameters for filtering: `@app.get("/items?skip=0&limit=10")`
- Return appropriate HTTP status codes

### Request/Response Models
```python
from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    description: str | None = None

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str | None

@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    # Create item logic
    return ItemResponse(id=1, name=item.name, price=item.price, description=item.description)
```

### Dependency Injection
```python
from fastapi import Depends, HTTPException, status
from typing import Annotated

def get_current_user(token: str = Header(...)) -> User:
    # Validate token and return user
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

@app.get("/me")
def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
```

### Error Handling
```python
from fastapi import HTTPException, status

@app.get("/items/{item_id}")
def read_item(item_id: int):
    item = get_item_from_db(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    return item
```

## Testing with pytest

### Test File Organization
- Name test files: `test_<module_name>.py` (e.g., `test_api.py`, `test_util.py`)
- Place tests at project root or in a `tests/` directory
- Group related tests with comment separators: `# --- function_name ---`

### Test Function Naming
- Pattern: `test_<function_name>_<scenario>`
- Be descriptive: `test_add_positive_numbers`, `test_api_returns_404_for_missing_item`
- Use clear scenario descriptions

### Testing API Endpoints
```python
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_read_item_returns_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["item_id"] == 1

def test_read_item_with_invalid_id_returns_404():
    response = client.get("/items/999")
    assert response.status_code == 404
```

### Testing Business Logic
```python
import pytest

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(5, 0)

def test_is_even_with_even_number():
    assert is_even(4) is True
```

### Test Coverage
- Write tests for:
  - Happy path (expected usage)
  - Edge cases (empty inputs, boundary values, zero)
  - Error cases (invalid inputs, exceptions)
  - All API endpoints (success and error responses)
- Use fixtures for common setup
- Mock external dependencies (databases, APIs)

### pytest Fixtures
```python
import pytest

@pytest.fixture
def sample_user():
    return User(id=1, email="test@example.com", name="Test User")

@pytest.fixture
def db_session():
    # Setup database
    session = create_test_session()
    yield session
    # Teardown
    session.close()

def test_create_user(db_session):
    user = create_user(db_session, "test@example.com")
    assert user.email == "test@example.com"
```

## Environment Configuration

### Setup
```python
import os
from dotenv import load_dotenv

# Load at module level
load_dotenv()

API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

### Best Practices
- Never commit `.env` files (add to `.gitignore`)
- Provide `.env.example` with dummy values
- Document all required environment variables in README
- Use type conversion for non-string values
- Provide sensible defaults where appropriate

## Database Integration

### SQLAlchemy Setup
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
```

### Database Dependency
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Security Best Practices

- **Authentication**: Use OAuth2, JWT tokens
- **Authorization**: Implement role-based access control (RBAC)
- **Input Validation**: Leverage Pydantic models
- **SQL Injection**: Use parameterized queries (SQLAlchemy ORM)
- **CORS**: Configure properly for production
- **Secrets**: Never hardcode; use environment variables
- **HTTPS**: Enforce in production
- **Rate Limiting**: Implement for public APIs

### CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Error Handling

### Custom Exceptions
```python
class ItemNotFoundError(Exception):
    """Raised when an item is not found."""
    pass

def get_item(item_id: int) -> Item:
    item = find_item(item_id)
    if not item:
        raise ItemNotFoundError(f"Item {item_id} not found")
    return item
```

### Exception Handlers
```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )
```

## Dependency Management

### pyproject.toml
```toml
[project]
name = "my-api"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.135.1",
    "uvicorn>=0.32.0",
    "python-dotenv>=1.2.2",
    "sqlalchemy>=2.0.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
test = [
    "pytest>=9.0.2",
    "httpx>=0.27.0",  # For TestClient
]
dev = [
    "black",
    "ruff",
    "mypy",
]
```

### Installation
```bash
pip install -e .                    # Install package
pip install -e ".[test]"           # Install with test dependencies
pip install -e ".[dev]"            # Install with dev dependencies
```

## Running the Application

### Development
```bash
uvicorn api:app --reload            # With auto-reload
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Python Script
```python
# main.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
```

## Performance Optimization

- Use async endpoints for I/O-bound operations:
  ```python
  @app.get("/items")
  async def read_items():
      items = await fetch_items_from_db()
      return items
  ```
- Implement caching for frequently accessed data
- Use connection pooling for databases
- Profile slow endpoints and optimize queries
- Consider background tasks for long-running operations:
  ```python
  from fastapi import BackgroundTasks
  
  @app.post("/send-email")
  def send_email(background_tasks: BackgroundTasks):
      background_tasks.add_task(send_email_task)
      return {"message": "Email queued"}
  ```

## Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/items/{item_id}")
def read_item(item_id: int):
    logger.info(f"Fetching item {item_id}")
    try:
        item = get_item(item_id)
        return item
    except Exception as e:
        logger.error(f"Error fetching item {item_id}: {e}")
        raise
```

## General Best Practices

- **Single Responsibility**: Keep functions focused on one task
- **DRY Principle**: Don't repeat yourself; extract common logic
- **Explicit > Implicit**: Write clear, self-documenting code
- **Type Safety**: Leverage Python's type hints and Pydantic
- **Error Messages**: Provide clear, actionable error messages
- **API Documentation**: FastAPI auto-generates docs at `/docs` and `/redoc`
- **Version Control**: Commit often with descriptive messages
- **Code Reviews**: Follow team review processes
- **Testing**: Write tests before or alongside new features
- **Refactoring**: Keep code clean and maintainable