# marimo-sphinx

[![PyPI version](https://badge.fury.io/py/marimo-sphinx.svg)](https://badge.fury.io/py/marimo-sphinx)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A Sphinx extension that adds interactive [Marimo](https://marimo.io) notebook buttons to API documentation.

Inspired by [jupyterlite-sphinx](https://github.com/jupyterlite/jupyterlite-sphinx), this extension embeds Marimo (WASM) directly in your Sphinx documentation via `marimo.app`.

## Features

- `.. marimo::` directive for explicit inline notebooks
- Automatic button injection into docstring `Examples` sections via `global_enable_marimo_examples`
- Lazy-loading iframe (button click → Marimo loads)

## Installation

```bash
pip install marimo-sphinx
```

## Usage

### In `conf.py`

```python
extensions = ["marimo_sphinx"]

# Optional: auto-inject buttons into all docstring Examples sections
global_enable_marimo_examples = True
marimo_global_button_text = "Try in Marimo"
marimo_global_height = "400px"
```

### Explicit directive

```rst
.. marimo::
   :height: 500px

   import marimo as mo
   x = mo.slider(1, 10, value=5)
   mo.md(f"Value: {x.value}")
```

### Docstring auto-detection

When `global_enable_marimo_examples = True`, examples in docstrings are
automatically converted:

```python
def my_function(x):
    """
    Examples
    --------
    >>> import marimo as mo
    >>> x = mo.slider(1, 10)
    """
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, release process, and contribution guidelines.

## License

MIT
