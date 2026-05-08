# PyNutil documentation

This repository contains the Sphinx documentation for
[PyNutil](https://github.com/Neural-Systems-at-UIO/PyNutil).

## Build locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make html
```

When this repository is checked out next to the main `PyNutil` repository, the
documentation build uses that local source tree for API documentation. Set
`PYNUTIL_SOURCE_PATH=/path/to/PyNutil` to point at a different checkout.
