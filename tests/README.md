# Tests for GWASTutorial

This directory contains test cases for each module in the GWASTutorial project.

## Test Structure

Tests are organized by module:
- `test_01_dataset.py` - Tests for dataset operations and missing value handling
- `test_04_data_qc.py` - Tests for data quality control operations
- `test_05_pca.py` - Tests for principal component analysis
- `test_06_association_tests.py` - Tests for association testing
- `test_10_prs_extract.py` - Tests for PRS extraction module
- `test_13_heritability.py` - Tests for heritability calculations
- `test_15_winners_curse.py` - Tests for winner's curse correction
- `test_50_step_by_step.py` - Tests for step-by-step genetic statistics

## Running Tests

### Install Dependencies

```bash
pip install -r tests/requirements.txt
```

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test Module

```bash
pytest tests/test_10_prs_extract.py
```

### Run with Verbose Output

```bash
pytest tests/ -v
```

### Run with Coverage

```bash
pytest tests/ --cov=. --cov-report=html
```

## Test Fixtures

The `conftest.py` file provides shared fixtures:
- `temp_dir` - Temporary directory for test files
- `sample_plink_data` - Sample PLINK data files
- `sample_gwas_data` - Sample GWAS summary statistics
- `sample_genotype_data` - Sample genotype data

## Adding New Tests

When adding tests for a new module:
1. Create a new test file following the naming convention `test_<module>_<name>.py`
2. Import necessary fixtures from `conftest.py`
3. Write test classes and methods following pytest conventions
4. Use descriptive test names that explain what is being tested
