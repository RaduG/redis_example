ENV_BIN_DIR=venv/bin
CODE_DIR=project
TESTS_DIR=tests

setup_environment:
	@echo "Creating virtual environment..."
	@python -m venv venv
	@echo "Installing requirements..."
	@${ENV_BIN_DIR}/pip install --upgrade pip
	@${ENV_BIN_DIR}/pip install -r requirements.txt
	@${ENV_BIN_DIR}/pip install -r requirements_dev.txt
	@${ENV_BIN_DIR}/pip install -r requirements_test.txt
	@echo "Installing pre-commit hook..."
	@${ENV_BIN_DIR}/pre-commit install

run_tests:
	@${ENV_BIN_DIR}/pytest ${TEST_PATH} --cov=${CODE_DIR}

generate_docs:
	@python -m pdoc ${CODE_DIR} -o docs