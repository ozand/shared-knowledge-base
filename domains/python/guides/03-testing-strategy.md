---
title: "Testing Strategy"
version: "1.0.0"
last_updated: "2025-01-01"
category: "quality_assurance"
priority: contextual
applies_to: ["all_projects"]
agent_usage: "Reference when writing tests or setting up test infrastructure"
keywords: ["testing", "pytest", "playwright", "unit", "integration", "e2e", "coverage"]
related_docs: ["01-project-structure.md", "02-code-quality.md"]
---

# Testing Strategy

> Comprehensive testing approach from unit to end-to-end

## Testing Pyramid

```
        /\
       /  \
      / E2E \    ← Few, slow, critical journeys
     /-------\
    /  INTEG  \  ← Moderate, component interactions
   /-----------\
  /    UNIT     \ ← Many, fast, isolated tests
 /_______________\
```

### Philosophy

- **Unit tests:** Many, fast, test individual components
- **Integration tests:** Moderate, test component interactions
- **E2E tests:** Few, slow, validate critical user journeys
- **Avoid exhaustive E2E testing** - save it for critical paths

---

## Unit Testing

### Purpose
- Test individual functions/classes in isolation
- No external dependencies (DB, network, filesystem)
- Fast execution (milliseconds per test)

### Location & Structure
```
tests/unit/
├── payments/
│   ├── test_processor.py
│   └── test_models.py
└── search/
    └── test_engine.py
```

Mirror `src/` structure exactly.

### Example

```python
# src/project_name/payments/processor.py
def calculate_fee(amount: float, rate: float) -> float:
    """Calculate processing fee."""
    if amount < 0:
        raise ValueError("Amount must be positive")
    return amount * rate


# tests/unit/payments/test_processor.py
import pytest
from src.project_name.payments.processor import calculate_fee


def test_calculate_fee_positive_amount():
    assert calculate_fee(100.0, 0.03) == 3.0


def test_calculate_fee_zero_amount():
    assert calculate_fee(0.0, 0.03) == 0.0


def test_calculate_fee_negative_amount_raises():
    with pytest.raises(ValueError, match="Amount must be positive"):
        calculate_fee(-100.0, 0.03)
```

### Best Practices

1. **One assert per test** (when possible)
2. **Clear test names:** `test_<action>_<condition>_<expected_outcome>()`
3. **AAA pattern:** Arrange, Act, Assert
4. **Use fixtures** for common setup
5. **Mock external dependencies:**

```python
from unittest.mock import Mock, patch

@patch('src.project_name.payments.processor.stripe_api')
def test_process_payment_calls_stripe(mock_stripe):
    mock_stripe.charge.return_value = {"id": "ch_123"}
    
    result = process_payment(100.0, "tok_visa")
    
    mock_stripe.charge.assert_called_once_with(
        amount=10000,
        source="tok_visa"
    )
```

---

## Integration Testing

### Purpose
- Test component interactions
- Verify API contracts
- Test database operations
- Test external service integrations

### Location
```
tests/integration/
├── test_api_routes.py
├── test_database.py
└── test_external_services.py
```

### Example: API Endpoint Test

```python
import pytest
from fastapi.testclient import TestClient
from src.project_name.api import app

client = TestClient(app)


def test_create_payment_success():
    response = client.post("/payments", json={
        "amount": 100.0,
        "currency": "USD",
        "token": "tok_visa"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "succeeded"
    assert "id" in data


def test_create_payment_invalid_token():
    response = client.post("/payments", json={
        "amount": 100.0,
        "currency": "USD",
        "token": "invalid"
    })
    
    assert response.status_code == 400
    assert "Invalid token" in response.json()["detail"]
```

### Database Testing

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="function")
def db_session():
    """Create isolated test database session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)


def test_create_user(db_session):
    user = User(email="test@example.com", name="Test User")
    db_session.add(user)
    db_session.commit()
    
    saved_user = db_session.query(User).filter_by(email="test@example.com").first()
    assert saved_user is not None
    assert saved_user.name == "Test User"
```

---

## E2E Testing with Playwright

### Setup

```bash
# Install dependencies
uv add --dev pytest pytest-playwright

# Install browser binaries
uv run playwright install
```

### Directory Structure

```
tests/e2e/
├── pages/                  # Page Object Model
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   ├── checkout_page.py
│   └── dashboard_page.py
├── data/                   # Test data
│   ├── users.json
│   └── products.json
├── conftest.py             # Shared fixtures
├── test_authentication.py
└── test_checkout_flow.py
```

### Page Object Model

```python
# tests/e2e/pages/base_page.py
class BasePage:
    def __init__(self, page):
        self.page = page
    
    def navigate_to(self, url: str):
        self.page.goto(url)
    
    def wait_for_selector(self, selector: str):
        self.page.wait_for_selector(selector)


# tests/e2e/pages/login_page.py
from .base_page import BasePage

class LoginPage(BasePage):
    # Selectors
    EMAIL_INPUT = '[data-testid="email"]'
    PASSWORD_INPUT = '[data-testid="password"]'
    LOGIN_BUTTON = '[data-testid="login-btn"]'
    ERROR_MESSAGE = '[data-testid="error"]'
    
    def login(self, email: str, password: str):
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)
    
    def get_error_message(self) -> str:
        return self.page.text_content(self.ERROR_MESSAGE)
```

### E2E Test Example

```python
# tests/e2e/test_authentication.py
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


def test_login_with_valid_credentials_succeeds(page: Page):
    """User can log in with valid email and password."""
    login_page = LoginPage(page)
    
    # Navigate to login
    login_page.navigate_to("https://app.example.com/login")
    
    # Perform login
    login_page.login("user@example.com", "correct_password")
    
    # Verify redirect to dashboard
    expect(page).to_have_url("https://app.example.com/dashboard")
    expect(page.locator('[data-testid="user-menu"]')).to_be_visible()


def test_login_with_invalid_credentials_shows_error(page: Page):
    """User sees error message with invalid credentials."""
    login_page = LoginPage(page)
    
    login_page.navigate_to("https://app.example.com/login")
    login_page.login("user@example.com", "wrong_password")
    
    # Verify error message
    error = login_page.get_error_message()
    assert "Invalid email or password" in error
```

### Data Isolation

**CRITICAL:** Each test must create its own data

```python
# ❌ Bad - relies on shared data
def test_user_can_checkout():
    # Assumes user "test@example.com" exists
    login("test@example.com", "password123")
    # ...


# ✅ Good - creates own test data
@pytest.fixture
def test_user(api_client):
    """Create isolated test user via API."""
    user = api_client.create_user({
        "email": f"test_{uuid.uuid4()}@example.com",
        "password": "Test123!"
    })
    yield user
    api_client.delete_user(user.id)


def test_user_can_checkout(page: Page, test_user):
    login_page = LoginPage(page)
    login_page.login(test_user.email, "Test123!")
    # ...
```

### Selector Priority

1. **User-facing attributes** (best):
```python
page.click('role=button[name="Submit"]')
page.fill('label=Email', 'user@example.com')
```

2. **Test IDs** (good):
```python
page.click('[data-testid="submit-btn"]')
```

3. **Stable attributes** (acceptable):
```python
page.click('[aria-label="Close dialog"]')
```

4. **Avoid** (brittle):
```python
page.click('.btn-primary.mt-4')  # ❌ CSS classes
page.click('//div[3]/button[2]')  # ❌ XPath by position
```

### No Hardcoded Waits

```python
# ❌ Bad - fixed delay
import time
page.click('[data-testid="submit"]')
time.sleep(5)  # Hope it loads in 5 seconds
page.click('[data-testid="confirm"]')


# ✅ Good - wait for specific condition
page.click('[data-testid="submit"]')
expect(page.locator('[data-testid="confirm"]')).to_be_visible()
page.click('[data-testid="confirm"]')


# ✅ Good - Playwright auto-waits
page.click('[data-testid="submit"]')
page.click('[data-testid="confirm"]')  # Auto-waits for element
```

---

## Test Execution

### Run All Tests

```bash
# All tests
uv run pytest

# Specific test type
uv run pytest tests/unit/
uv run pytest tests/integration/
uv run pytest tests/e2e/
```

### Run with Coverage

```bash
# Generate coverage report
uv run pytest --cov=src --cov-report=html --cov-report=term

# Enforce minimum coverage
uv run pytest --cov=src --cov-fail-under=80
```

### Run Specific Tests

```bash
# By file
uv run pytest tests/unit/payments/test_processor.py

# By test name
uv run pytest tests/unit/ -k "test_calculate_fee"

# By marker
uv run pytest -m slow
```

### E2E with Tracing

```bash
# Enable tracing for debugging
uv run pytest tests/e2e/ --tracing on

# Open trace viewer
uv run playwright show-trace trace.zip
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - run: uv sync
      - run: uv run pytest tests/unit/ --cov=src

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - run: uv sync
      - run: uv run pytest tests/integration/

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - run: uv sync
      - run: uv run playwright install --with-deps
      - run: uv run pytest tests/e2e/ --tracing on
      
      - name: Upload artifacts on failure
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-traces
          path: test-results/
```

---

## Coverage Requirements

| Test Type | Coverage Target | Why |
|-----------|----------------|-----|
| Unit | ≥80% | Core business logic must be tested |
| Integration | ≥60% | Key integrations verified |
| E2E | Critical paths only | Full user journeys for essential features |

### Measuring Coverage

```bash
# Generate HTML report
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html

# Show missing lines
uv run pytest --cov=src --cov-report=term-missing

# XML report (for CI tools)
uv run pytest --cov=src --cov-report=xml
```

---

## Debugging Failed Tests

### Playwright Trace Viewer

```bash
# Run with tracing
uv run pytest tests/e2e/ --tracing on

# Open specific trace
uv run playwright show-trace test-results/test-login-chromium/trace.zip
```

**Trace includes:**
- Screenshots at each step
- Network activity
- Console logs
- Action timeline

### pytest Debugging

```bash
# Show print statements
uv run pytest -s

# Drop into debugger on failure
uv run pytest --pdb

# Show local variables on failure
uv run pytest -l

# Verbose output
uv run pytest -vv
```

---

## Flaky Test Management

**Flaky test:** Passes and fails intermittently without code changes

### Prevention

1. **Avoid race conditions:** Use explicit waits
2. **Isolate test data:** Each test creates own data
3. **Reset state:** Clean up after each test
4. **Avoid external dependencies:** Use mocks/stubs

### Detection

```bash
# Run tests multiple times
uv run pytest tests/ --count=10
```

### Resolution

1. **Investigate:** Use trace viewer to find root cause
2. **Fix immediately:** Flaky tests erode confidence
3. **Quarantine if needed:** Mark with `@pytest.mark.skip` temporarily
4. **Remove if unfixable:** Better no test than flaky test

---

## Test Maintenance

### Regular Tasks

- **Weekly:** Review and fix flaky tests
- **Monthly:** Update test data and fixtures
- **Per release:** Audit E2E test coverage of new features
- **Quarterly:** Refactor test utilities and helpers

### When to Delete Tests

- Test for removed feature
- Redundant coverage (testing same thing multiple ways)
- Unmaintainable or consistently flaky
- Testing framework internals (not your code)
