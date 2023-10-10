# Use Python 3.11 as the base image
FROM python:3.11 AS base

# Set environment variables
ENV NODE_OPTIONS=--openssl-legacy-provider
ENV CHROMEDRIVER_VERSION 115.0.5790.98
ENV CHROMEDRIVER_URL https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip
ENV POETRY_VERSION=1.6.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Configure and install Poetry
RUN python3 -m venv $POETRY_VENV && \
    $POETRY_VENV/bin/pip install -U pip setuptools && \
    $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Install Python dependencies with Poetry
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install

# Copy the rest of the app and set ports and default command
COPY . .
EXPOSE 80 443 8080
CMD [ "poetry", "run", "python", "-m", "run" ]
