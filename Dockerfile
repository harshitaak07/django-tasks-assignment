FROM python:3.12-slim-bookworm

# Set environment variables
ENV SECRET_KEY=secret
ENV DEBUG=True
ENV DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
ENV REDIS_URL=redis://:A5so9VpQ6Q5wF2ogOgTOIucNBftHLaZe@redis-11690.crce194.ap-seast-1-1.ec2.redns.redis-cloud.com:11690

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .