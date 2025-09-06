# Test Structure Documentation

This document describes the organized test structure for the Cinetica physics library.

## Directory Structure

```
tests/
├── __init__.py
├── README.md                          # This documentation
├── unit/                              # Unit tests for individual components
│   ├── __init__.py
│   ├── test_cinetica.py              # Main library tests (version, imports)
│   └── cinematica/                    # Physics module tests
│       ├── __init__.py
│       ├── test_base_movimiento.py   # Abstract base class tests
│       ├── rectilineo/               # Linear motion tests
│       │   ├── __init__.py
│       │   ├── test_movimiento_rectilineo.py
│       │   ├── test_units_mru.py
│       │   └── test_units_mruv.py
│       ├── circular/                 # Circular motion tests
│       │   ├── __init__.py
│       │   ├── test_movimiento_circular.py
│       │   └── test_units_circular.py
│       ├── parabolico/               # Projectile motion tests
│       │   ├── __init__.py
│       │   ├── test_movimiento_parabolico.py
│       │   └── test_units_parabolico.py
│       ├── oscilatorio/              # Oscillatory motion tests
│       │   ├── __init__.py
│       │   ├── test_movimiento_oscilatorio.py
│       │   ├── test_movimiento_armonico_complejo.py
│       │   ├── test_units_oscilatorio.py
│       │   └── test_units_armonico_complejo.py
│       ├── espacial/                 # 3D motion tests
│       │   ├── __init__.py
│       │   ├── test_movimiento_espacial.py
│       │   └── test_units_espacial.py
│       ├── relativo/                 # Relative motion tests
│       │   ├── __init__.py
│       │   ├── test_movimiento_relativo.py
│       │   └── test_units_relativo.py
│       └── graficos/                 # Graphics/plotting tests
│           ├── __init__.py
│           └── test_graficos.py
├── comprehensive/                     # Comprehensive test suites
│   ├── __init__.py
│   ├── test_mruv_comprehensive.py    # Extensive MRUV testing
│   └── test_mcu_comprehensive.py     # Extensive MCU testing
└── integration/                      # Integration tests (future use)
    └── __init__.py
```

## Test Categories

### Unit Tests (`tests/unit/`)
- **Purpose**: Test individual components and methods in isolation
- **Scope**: Single classes, methods, or functions
- **Coverage**: Basic functionality, edge cases, error handling
- **Examples**: Testing MRU position calculation, unit conversions, parameter validation

### Comprehensive Tests (`tests/comprehensive/`)
- **Purpose**: Extensive testing of complex modules with multiple scenarios
- **Scope**: Complete module functionality with physics validation
- **Coverage**: Edge cases, physics consistency, performance, integration between methods
- **Examples**: Complete MRUV testing with kinematic equation validation, MCU vector methods

### Integration Tests (`tests/integration/`)
- **Purpose**: Test interactions between different modules (future expansion)
- **Scope**: Multi-module workflows and data flow
- **Coverage**: Module interactions, end-to-end scenarios
- **Status**: Reserved for future development

## Test Naming Conventions

### File Naming
- `test_*.py` - Standard pytest discovery pattern
- `test_units_*.py` - Tests specifically for unit handling and conversions
- `test_*_comprehensive.py` - Comprehensive test suites for complex modules

### Test Method Naming
- `test_<functionality>` - Basic functionality tests
- `test_<functionality>_edge_case` - Edge case testing
- `test_<functionality>_error_handling` - Error condition testing
- `test_<functionality>_with_units` - Unit-specific testing

## Running Tests

### All Tests
```bash
python -m pytest
```

### Specific Categories
```bash
# Unit tests only
python -m pytest tests/unit/

# Comprehensive tests only
python -m pytest tests/comprehensive/

# Specific module tests
python -m pytest tests/unit/cinematica/rectilineo/

# With coverage
python -m pytest --cov=cinetica --cov-report=term-missing
```

### Test Discovery
Pytest automatically discovers tests following these patterns:
- Files: `test_*.py` or `*_test.py`
- Classes: `Test*`
- Functions: `test_*`

## Coverage Goals

- **Overall Target**: >95% code coverage
- **Unit Tests**: Focus on individual method coverage
- **Comprehensive Tests**: Focus on physics validation and edge cases
- **Integration Tests**: Focus on module interaction coverage

## Current Status

- **Total Tests**: 228
- **Coverage**: 97%
- **Modules Covered**: All physics modules with comprehensive testing
- **Test Structure**: Fully organized and maintainable

## Adding New Tests

### For New Features
1. Add unit tests in appropriate `tests/unit/cinematica/<module>/` directory
2. Include both functionality and unit handling tests
3. Add comprehensive tests in `tests/comprehensive/` for complex features

### Test Requirements
- All tests must pass
- New code must maintain >95% coverage
- Include edge cases and error handling
- Follow physics validation patterns for kinematic equations

## Maintenance

- Keep test structure aligned with source code organization
- Update this documentation when adding new test categories
- Regularly review and refactor tests for maintainability
- Ensure test isolation and independence
