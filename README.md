# python_template
This Python template is aimed at bootstraping any new Python project with the structure and
the tools necessary to start writing good Python code.

Please note that the included dependencies **are not pinned** just because I plan to not really
update this repository for new versions, unless something major changes.

## Features
* individual requirements files (disjoint):
  + `requirements.txt` - the packages required **to run** the code
  + `requirements_dev.txt` - the packages required **to set up a development environment**
  + `requirements_test.txt` - the packages required **to run the tests**
  + `requirements_build.txt` - the packages required **to build the package**

* a `Makefile` which implements three tasks:
  + `setup_environment` - creates a `venv`, installs **all** the requirements and sets up the `pre-commit` hooks
  + `run_tests` - pretty much what it says on the tin (`pytest` + `pytest-cov`)
  + `generate_docs` - generates code documentation using `pdoc3` in Markdown format under `docs/`

* pre-commit hooks using `pre-commit`:
  + `isort` - changes files in-place and adds them back to the commit
  + `black` - changes files in-place and adds them back to the commit
  + `flake8` - uses the included minimal configuration
  + `mypy`
  + `pytest` with `pytest-cov`

## Getting started
* Fork the repository
* Create a new repository based on it as a template
* Clone the new repository
* Rename `project/` to something more appropriate
* Change `project/` to the new path in `Makefile` and `pre-commit-config.yaml`
* Run `make setup_environment`
* Build something awesome