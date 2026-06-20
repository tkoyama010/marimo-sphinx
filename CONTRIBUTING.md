# Contributing to marimo-sphinx

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/tkoyama010/marimo-sphinx.git
   cd marimo-sphinx
   ```

2. Install in development mode with test dependencies:
   ```bash
   pip install -e ".[test]"
   ```

3. Run tests:
   ```bash
   pytest -v
   ```

## Release Process

This project uses [Release Please](https://github.com/googleapis/release-please) for automated version management and changelog generation, combined with automated PyPI publishing.

### How it works

1. **Commit with Conventional Commits**: Use commit messages that follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
   - `feat:` for new features (bumps minor version)
   - `fix:` for bug fixes (bumps patch version)
   - `feat!:` or `fix!:` with `BREAKING CHANGE:` in body for breaking changes (bumps major version)
   - Other types: `docs:`, `style:`, `refactor:`, `test:`, `chore:`

2. **Automated Release PR**: When changes are merged to `main`, Release Please automatically creates or updates a release PR that:
   - Updates version in `pyproject.toml`
   - Updates `CHANGELOG.md`
   - Creates a GitHub release when merged

3. **Automated PyPI Publishing**: When the release PR is merged and a GitHub release is created:
   - The package is automatically built
   - Published to PyPI via OIDC trusted publisher (no API tokens needed)

### First-time PyPI Setup

To enable automated publishing, a repository maintainer must configure PyPI's trusted publisher:

1. Create a PyPI account at https://pypi.org if you don't have one

2. Go to https://pypi.org/manage/account/publishing/ and add a "pending publisher":
   - **PyPI Project Name**: `marimo-sphinx`
   - **Owner**: `tkoyama010`
   - **Repository name**: `marimo-sphinx`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`

3. Create the `pypi` environment in GitHub repository settings:
   - Go to repository Settings → Environments → New environment
   - Name: `pypi`
   - Add protection rules if desired (e.g., require review)

4. After the first successful publish, the pending publisher becomes an active trusted publisher

### Manual Release (if needed)

If you need to publish manually:

1. Install build dependencies:
   ```bash
   pip install build
   ```

2. Build the package:
   ```bash
   python -m build
   ```

3. Upload to PyPI (requires PyPI API token):
   ```bash
   pip install twine
   twine upload dist/*
   ```

### Testing on TestPyPI

To test the release process on TestPyPI first:

1. Configure TestPyPI trusted publisher at https://test.pypi.org/manage/account/publishing/

2. Modify `.github/workflows/publish.yml` temporarily to use TestPyPI:
   ```yaml
   - name: Publish package distributions to TestPyPI
     uses: pypa/gh-action-pypi-publish@release/v1
     with:
       repository-url: https://test.pypi.org/legacy/
   ```

3. After testing, revert the workflow to use production PyPI

## Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to public functions and classes
- Keep functions focused and small

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Tests are located in the `tests/` directory
- Run tests with: `pytest -v`
