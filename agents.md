# Agent Guidelines for cicd-demo Project

## Framework & Dependencies

- **Web Framework**: Use FastAPI for all API endpoints
- **Testing Framework**: Use pytest for all tests
- **Environment Configuration**: Use python-dotenv to load environment variables from `.env` files
- **Python Version**: Maintain compatibility with Python 3.12+
- **Dependency Management**: Add dependencies to `pyproject.toml` under `[project.dependencies]` or `[project.optional-dependencies]`

## Code Style & Conventions

### Naming
- Use **snake_case** for functions, variables, and file names
- Use descriptive names that clearly indicate purpose (e.g., `read_item`, `health_check`, `is_palindrome`)

### Type Hints
- Use type hints for function parameters and return types
- Use modern Python 3.10+ syntax: `str | None` instead of `Optional[str]`
- Example: `def read_item(item_id: int, q: str | None = None):`

### Documentation
- Include docstrings for all public functions
- Use Google-style docstrings
- Document parameters, return values, and exceptions
- Example:
  ```python
  def divide(a, b):
      """Return the quotient of a divided by b.

      Raises:
          ValueError: If b is zero.
      """
  ```

### Code Organization
- Keep related functionality in separate modules (e.g., `api.py`, `util.py`)
- Maintain flat project structure (avoid over-engineering with nested packages)
- Place environment variable loading at the top of files that need it
- Use clear separation: utilities in `util.py`, API routes in `api.py`, entry points in `main.py`

## API Development (FastAPI)

### Structure
- Initialize FastAPI app: `app = FastAPI()`
- Group related endpoints logically
- Always include a `/health` endpoint for health checks

### Endpoints
- Use RESTful conventions
- Return simple JSON dictionary responses: `{"key": "value"}`
- Use path parameters for resources: `@app.get("/items/{item_id}")`
- Use query parameters for optional filters: `q: str | None = None`

### Responses
- Keep responses simple and consistent
- Use dictionaries with clear, descriptive keys
- Example: `{"status": "ok"}`, `{"message": "Hello FastAPI"}`

## Testing with pytest

### Test File Organization
- Name test files: `test_<module_name>.py` (e.g., `test_util.py`)
- Place tests at the project root (same level as source files)
- Group related tests with comment separators: `# --- function_name ---`

### Test Function Naming
- Pattern: `test_<function_name>_<scenario>`
- Be descriptive: `test_add_positive_numbers`, `test_divide_by_zero_raises`
- Use clear scenario descriptions

### Test Coverage
- Write multiple test cases per function covering:
  - Happy path (normal expected usage)
  - Edge cases (zero, empty strings, boundary values)
  - Error cases (invalid inputs, exceptions)
- Test both positive and negative scenarios

### Testing Exceptions
- Use `pytest.raises` for exception testing
- Include match parameter for exception messages:
  ```python
  with pytest.raises(ValueError, match="Cannot divide by zero"):
      divide(5, 0)
  ```

### Assertions
- Use simple `assert` statements
- Test for exact equality when appropriate: `assert add(2, 3) == 5`
- Use `is True` / `is False` for boolean tests: `assert is_even(4) is True`

## Environment Configuration

- Load environment variables using `dotenv.load_dotenv()` at module level
- Access variables with `os.getenv("VAR_NAME")`
- Never commit `.env` files (they should be in `.gitignore`)
- Document required environment variables in README

## Error Handling

- Raise descriptive exceptions with clear messages
- Use appropriate exception types (ValueError, TypeError, etc.)
- Document raised exceptions in docstrings

## General Best Practices

- Keep functions small and focused (single responsibility)
- Write self-documenting code with clear names
- Test-driven development: write tests for new functionality
- Follow Python's "explicit is better than implicit" principle
- Use modern Python features (3.12+ compatible)
- Keep dependencies minimal and purposeful
