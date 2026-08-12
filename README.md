# SauceDemo Week 4 POM Framework

This repository includes a Playwright-based SauceDemo Page Object Model framework with environment-based configuration, dynamic test data, and a GitHub Actions CI workflow.

## Folder structure

- `sauceDemo_week4/`
  - `pages/` - Page Object Model classes for SauceDemo pages
  - `tests/` - Pytest test flows for SauceDemo
  - `config.py` - Environment-driven test settings
  - `conftest.py` - Playwright fixtures and Faker test data
  - `pytest.ini` - Pytest configuration and report settings
  - `requirements.txt` - Pinned Python dependencies
  - `.env.example` - Example environment variables

## Setup

1. Copy the example environment file:

   ```bash
   cp sauceDemo_week4/.env.example sauceDemo_week4/.env
   ```

2. Update `sauceDemo_week4/.env` if you need to override defaults.

3. Install dependencies:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r sauceDemo_week4/requirements.txt
   ```

4. Install Playwright browsers:

   ```bash
   python -m playwright install --with-deps
   ```

## Run tests locally

From the repository root:

```bash
cd sauceDemo_week4
pytest
```

Run tests in headed mode:

```bash
cd sauceDemo_week4
pytest --headed
```

## GitHub Actions CI

A workflow is configured in `.github/workflows/ui-tests.yml`. It installs dependencies, installs Playwright browsers, runs the pytest suite, and uploads the HTML report and screenshots as artifacts.
