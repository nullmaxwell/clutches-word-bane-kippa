# This Dockerfile creates a custom image based on this repo's environment.yml
FROM mambaorg/micromamba:latest
COPY --chown=$MAMBA_USER:$MAMBA_USER . .

# Micromamba base environment update
RUN micromamba install -y -n base -f prod_env.yml && micromamba clean --all --yes

# Reactivating the updated environment
SHELL [ "micromamba", "run", "-n", "base", "/bin/bash", "-c" ]


# Running the Dagit UI and Dagster daemon
CMD [ "micromamba", "run", "-n", "base", "src/main.py"]
