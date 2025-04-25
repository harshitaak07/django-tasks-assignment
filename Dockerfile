FROM python:3.12-slim-bookworm

# Set environment variables
ENV SECRET_KEY=secret
ENV DEBUG=True
ENV DATABASE_URL=postgres://postgres:postgres@db:5432/postgres

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .