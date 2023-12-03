#################################################################################
# Global Variables                                                              #
#################################################################################

PROFILE = default
PROJECT_NAME = clutches-word-bane-kippa
PYTHON_INTERPRETER = python3
PYTHON_VERSION = 3.12


ifeq (,$(shell which micromamba))
HAS_MICROMAMBA=False
else
HAS_MICROMAMBA=True
endif

#################################################################################
# Environment Commands                                                          #
#################################################################################

## Create a development micromamba environment.
dev_env:
ifeq (True,$(HAS_MICROMAMBA))
	@echo ">>> Detected micromamba, creating environment..."
	micromamba env create -f dev_env.yml
	@echo ">>> New micromamba environment created. Activate the new environment with:\n micromamba activate $(PROJECT_NAME) && micromamba init zsh"
else
	@echo ">>> micromamba not installed.\nPlease install micromamba and attempt again.\n
endif

## Create a production micromamba environment.
prod_env:
ifeq (True,$(HAS_MICROMAMBA))
	@echo ">>> Detected micromamba, creating environment..."
	micromamba env create -f prod_env.yml
	@echo ">>> New micromamba environment created. Activate the new environment with:\n micromamba activate $(PROJECT_NAME) && micromamba init zsh"
else
	@echo ">>> micromamba not installed.\nPlease install micromamba and attempt again.\n
endif

## Install Python Dependencies
requirements: test_env
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Removes all installed packages from the virtual environment.
clean_env:
	pip freeze | xargs pip uninstall -y

## Export the current environment.
env_update:
ifeq (True,$(HAS_MICROMAMBA))
	@echo ">>> Detected micromamba, exporting environment..."
	micromamba env export --no-builds > prod_env.yml && sed -i 's/$(PROJECT_NAME)/base/g' prod_env.yml
	@echo ">>> prod_env.yml successfully updated..."
	echo "-e ." > requirements.txt && pip list --format=freeze >> requirements.txt
	@echo ">>> requirements.txt successfully updated..."
else
	@echo ">>> micromamba not installed.\nPlease install micromamba and attempt again.\n
endif

## Remove the micromamba virtual environment for this project.
remove_env:
	micromamba env remove -n $(PROJECT_NAME)

#################################################################################
# General Development Commands                                                  #
#################################################################################

## Delete all compiled Python files and output files.
clean:
	rm -rf cache output/* .pytest_cache
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -wholename reports/*.html -delete

## Lint using flake8.
lint:
	flake8 src

#################################################################################
# Docker Commands                                                               #
#################################################################################

## Creates a Docker image of the application.
docker-image:
	docker build -t $(DOCKER_IMAGE_NAME) .