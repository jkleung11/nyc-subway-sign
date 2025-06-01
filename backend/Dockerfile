FROM python:3.12-slim AS base

# Install dependencies for installing pipx and Poetry
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install pipx
RUN pip install --no-cache-dir pipx \
    && pipx ensurepath

# Ensure Poetry is installed and available in the PATH
ENV PATH=/root/.local/bin:$PATH
RUN pipx install poetry==1.7.1

# Set the working directory
WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

# Stage for tests
FROM base AS test
RUN poetry install --with dev
COPY . /app
CMD ["poetry", "run", "pytest"]


# Stage for backend
FROM base AS backend
RUN poetry install --no-root
COPY . /app
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
