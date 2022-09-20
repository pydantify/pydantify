# Edit python version here.
# Note that only the major version should be specified, as pdm uses it as part
# of the path when installing.
ARG VERSION=3.10

################################################################################
#                                Builder stage                                 #
################################################################################
FROM python:${VERSION}-slim AS builder

ARG VERSION
WORKDIR /app

# Install required tools for building project.
# Git is optional here, but required if you have dependencies that need to be
# installed from git repos.
RUN apt update && \
    apt upgrade -y && \
    apt install -y --no-install-recommends git && \
    pip install -U pip setuptools wheel pdm

# Copy files required for building project.
COPY pyproject.toml pdm.lock README.md ./
COPY ./yang2pydantic/ ./yang2pydantic/

# Install dependencies and build project.
# Copy files to /my_pkgs/ for easier access in the production stage.
RUN pdm config python.use_venv False
RUN pdm install --prod --no-lock --no-editable -v && \
    cp -r ./__pypackages__/${VERSION}/lib /my_pkgs/


################################################################################
#                               Production stage                               #
################################################################################
FROM python:${VERSION}-slim AS production

WORKDIR /app

# Set python path so your project will be recognised as a valid module.
ENV PYTHONPATH=./pkgs

# Copy over your project and all its dependencies.
COPY --from=builder /my_pkgs ./pkgs

# Run your project as a module.
CMD ["python", "-m", "yang2pydantic"]
