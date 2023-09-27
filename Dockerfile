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

# Install required tools for adding repositories
RUN apt-get update && apt-get install -y wget gnupg2 software-properties-common && rm -rf /var/lib/apt/lists/*

# Add Chrome and Node repositories and keys
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/chrome-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/chrome-archive-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list > /dev/null && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -

# Install required packages
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends build-essential nodejs postgresql-client libpq-dev libvips poppler-utils pkg-config unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man

# Install Chromedriver
RUN wget -N $CHROMEDRIVER_URL -P ~/ && \
    unzip ~/chromedriver-linux64.zip -d ~/ && \
    rm ~/chromedriver-linux64.zip && \
    mv -f ~/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver

# Configure and install Poetry
RUN python3 -m venv $POETRY_VENV && \
    $POETRY_VENV/bin/pip install -U pip setuptools && \
    $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Install Python dependencies with Poetry
COPY poetry.lock pyproject.toml ./
RUN poetry install

# Copy the rest of the app and set ports and default command
COPY . .
EXPOSE 80 443
CMD [ "poetry", "run", "python", "-m", "run" ]
