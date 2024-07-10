FROM python:3.12-slim

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

# Copy only pyproject.toml and poetry.lock to leverage Docker cache
COPY pyproject.toml poetry.lock* /app/

# Install dependencies using Poetry
RUN poetry install --no-root

# Copy the rest of the application code
COPY . /app

# Set the entry point to use the virtual environment's Python interpreter
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
