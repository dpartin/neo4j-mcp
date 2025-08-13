# Contributing to Neo4j MCP Server

Thank you for your interest in contributing to the Neo4j MCP Server project! This document provides guidelines and information for contributors.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Git Workflow](#git-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Getting Started

### Prerequisites

- Python 3.9+
- Git
- Neo4j 5.x+ (for testing)
- nv (recommended) or virtual environment

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/neo4j_mcp.git
   cd neo4j_mcp
   ```

3. **Setup development environment**:
   ```bash
   # Using nv (recommended)
   python setup_dev.py
   
   # Or manual setup
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Setup Git**:
   ```bash
   python setup_git.py
   ```

5. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-owner/neo4j_mcp.git
   ```

## Git Workflow

### Branch Strategy

We use a feature branch workflow:

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches
- `hotfix/*` - Critical bug fixes

### Creating a Feature Branch

```bash
# Ensure you're on the main branch and it's up to date
git checkout main
git pull upstream main

# Create and switch to a new feature branch
git checkout -b feature/your-feature-name

# Or using the develop branch
git checkout develop
git pull upstream develop
git checkout -b feature/your-feature-name
```

### Making Changes

1. **Make your changes** in the feature branch
2. **Test your changes**:
   ```bash
   # Run all tests
   nv run pytest tests/ -v
   
   # Run specific tests
   nv run pytest tests/test_your_feature.py -v
   
   # Run with coverage
   nv run pytest --cov=neo4j_mcp_server
   ```

3. **Commit your changes**:
   ```bash
   # Add files
   git add .
   
   # Commit with a descriptive message
   git commit -m "feat: add new node creation functionality
   
   - Implement create_node tool with validation
   - Add comprehensive error handling
   - Include unit tests for new functionality
   
   Closes #123"
   ```

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat(nodes): add node validation functionality"
git commit -m "fix(connection): resolve Neo4j connection timeout issue"
git commit -m "docs: update API documentation for CRUD operations"
git commit -m "test(analytics): add comprehensive path finding tests"
```

### Keeping Your Branch Updated

```bash
# Fetch latest changes
git fetch upstream

# Rebase your feature branch on main
git checkout main
git pull upstream main
git checkout feature/your-feature-name
git rebase main

# Or merge main into your branch
git merge main
```

## Code Style

### Python Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: 88 characters (Black default)
- **Import sorting**: Use `isort`
- **Code formatting**: Use `black`

### Code Quality Tools

```bash
# Format code
nv run black neo4j_mcp_server/

# Sort imports
nv run isort neo4j_mcp_server/

# Lint code
nv run flake8 neo4j_mcp_server/

# Type checking
nv run mypy neo4j_mcp_server/
```

### Pre-commit Hooks

The project includes pre-commit hooks that run automatically:

- Python syntax check
- Basic test suite
- Code formatting check

To install pre-commit hooks manually:
```bash
git config core.hooksPath .git/hooks
```

## Testing

### Running Tests

```bash
# Run all tests
nv run pytest tests/ -v

# Run with coverage
nv run pytest --cov=neo4j_mcp_server --cov-report=html

# Run specific test categories
nv run pytest tests/test_crud.py -v
nv run pytest tests/test_analytics.py -v
nv run pytest tests/test_rag.py -v

# Run tests with markers
nv run pytest -m "unit" -v
nv run pytest -m "integration" -v
nv run pytest -m "slow" -v
```

### Writing Tests

- **Test file naming**: `test_*.py`
- **Test function naming**: `test_*`
- **Test class naming**: `Test*`
- **Use descriptive test names**
- **Include both positive and negative test cases**

**Example:**
```python
def test_create_node_with_valid_data():
    """Test creating a node with valid labels and properties."""
    # Arrange
    labels = ["Person"]
    properties = {"name": "Alice", "age": 30}
    
    # Act
    result = await create_node(labels, properties)
    
    # Assert
    assert result["success"] is True
    assert "node_id" in result
    assert result["labels"] == labels
    assert result["properties"] == properties


def test_create_node_with_invalid_labels():
    """Test creating a node with invalid labels raises error."""
    # Arrange
    labels = []  # Empty labels
    
    # Act & Assert
    with pytest.raises(ValidationError):
        await create_node(labels, {})
```

### Test Coverage

- **Minimum coverage**: 80%
- **Target coverage**: 90%+
- **Critical paths**: 100%

## Documentation

### Code Documentation

- **Docstrings**: Use Google style docstrings
- **Type hints**: Include for all functions
- **Comments**: Explain complex logic

**Example:**
```python
async def create_node(
    labels: List[str], 
    properties: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create a new node with labels and properties.
    
    Args:
        labels: List of node labels (e.g., ["Person", "Employee"])
        properties: Optional dictionary of node properties
        
    Returns:
        Dictionary containing operation result with node_id
        
    Raises:
        ValidationError: If labels are empty or invalid
        ConnectionError: If Neo4j connection fails
        QueryError: If Cypher query execution fails
        
    Example:
        >>> result = await create_node(["Person"], {"name": "Alice"})
        >>> print(result["node_id"])
        123
    """
```

### Documentation Files

- **README.md**: Project overview and quick start
- **TRD_Neo4j_MCP_Server.md**: Technical requirements
- **CONTRIBUTING.md**: This file
- **API.md**: API documentation (to be created)
- **CHANGELOG.md**: Version history (to be created)

## Pull Request Process

### Before Submitting

1. **Ensure tests pass**:
   ```bash
   nv run pytest tests/ -v
   nv run pytest --cov=neo4j_mcp_server
   ```

2. **Check code quality**:
   ```bash
   nv run black neo4j_mcp_server/
   nv run flake8 neo4j_mcp_server/
   nv run mypy neo4j_mcp_server/
   ```

3. **Update documentation** if needed

4. **Squash commits** if you have multiple commits:
   ```bash
   git rebase -i main
   ```

### Creating a Pull Request

1. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub** with:
   - **Clear title**: Brief description of changes
   - **Detailed description**: What, why, and how
   - **Related issues**: Link to issues being addressed
   - **Screenshots**: If UI changes are involved

3. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Code refactoring
   - [ ] Test addition/update

   ## Testing
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Manual testing completed

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] Tests added/updated
   - [ ] No breaking changes

   ## Related Issues
   Closes #123
   ```

### PR Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Address feedback** and update PR
4. **Merge** when approved

## Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10, macOS 12.0]
- Python: [e.g., 3.9.7]
- Neo4j: [e.g., 5.0.0]
- Package version: [e.g., 0.1.0]

## Additional Information
Screenshots, logs, etc.
```

### Feature Requests

Use the feature request template:

```markdown
## Feature Description
Clear description of the feature

## Use Case
Why this feature is needed

## Proposed Solution
How you think it should work

## Alternatives Considered
Other approaches you've considered

## Additional Information
Any other relevant information
```

## Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check README.md and TRD document first

## Code of Conduct

- Be respectful and inclusive
- Focus on the code, not the person
- Provide constructive feedback
- Help others learn and grow

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Neo4j MCP Server! 🚀
