# HDM Testing Framework

This directory contains the test suite for the HDM (Human Digital Memory) processing pipeline.

## Structure

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for complete workflows  
├── fixtures/       # Test data and fixtures
├── conftest.py     # Shared pytest fixtures
└── README.md       # This file
```

## Running Tests

### Using pytest directly:
```bash
# Run all tests
.venv/bin/pytest tests/

# Run only unit tests
.venv/bin/pytest tests/unit/

# Run only integration tests
.venv/bin/pytest tests/integration/

# Run with coverage
.venv/bin/pytest tests/ --cov=scripts.refactored --cov-report=html
```

### Using the test runner script:
```bash
# Run all tests
python run_tests.py

# Run only unit tests
python run_tests.py --type unit

# Run quietly
python run_tests.py --quiet
```

## Test Categories

### Unit Tests
- Test individual classes and functions in isolation
- Mock external dependencies
- Fast execution (< 1 second per test)
- High coverage of core functionality

### Integration Tests  
- Test complete workflows end-to-end
- Use real file system operations
- Test CLI integration
- Verify system interactions

## Writing Tests

### Test Naming
- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### Fixtures
Common fixtures are available in `conftest.py`:
- `temp_dir`: Temporary directory for file operations
- `sample_config`: Pre-configured Config object
- `sample_paper_data`: Sample paper metadata
- `sample_csv_data`: Sample CSV data

### Example Test
```python
def test_example_functionality(sample_config, temp_dir):
    """Test example functionality with fixtures."""
    # Setup
    processor = ExampleProcessor(sample_config)
    
    # Action
    result = processor.process_item("test_input")
    
    # Assert
    assert result.status == ProcessingStatus.COMPLETED
    assert result.data is not None
```

## Current Test Coverage

### Core Modules
- ✅ Config management
- ✅ Base processor functionality  
- ✅ Cleanup helper utilities

### Processors
- ⚠️ PDF converter (partial)
- ⚠️ Metadata extractor (partial)
- ⚠️ Data standardizer (partial)

### Pipelines
- ❌ Paper processing pipeline
- ❌ Data integration pipeline
- ❌ Quality assurance pipeline

### CLI
- ⚠️ Basic CLI integration (partial)

## Adding New Tests

1. Choose appropriate directory (`unit/` or `integration/`)
2. Create test file following naming convention
3. Import required modules and fixtures
4. Write descriptive test methods
5. Use appropriate assertions
6. Mock external dependencies for unit tests
7. Update this README if adding new test categories

## Dependencies

Required packages (installed via requirements-dev.txt):
- pytest
- pytest-mock
- pytest-cov (optional, for coverage)

## CI/CD Integration

Tests are designed to run in CI/CD environments:
- No external network dependencies (mocked)
- Temporary file cleanup
- Deterministic test results
- Parallel execution support