PYTHON = python3

UV = uv

FLAKE = flake8 src

MYPY = mypy src \
	--follow-imports=skip \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

.PHONY: install run debug clean lint

install:
	@$(UV) sync

run:
	@$(UV) run $(PYTHON) -m src

debug:
	@$(UV) run $(PYTHON) -m pdb -m src

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

lint:
	@$(UV) run $(FLAKE)
	@$(UV) run $(MYPY)