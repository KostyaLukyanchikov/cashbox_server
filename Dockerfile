# Pull official base image
FROM python:3.11-slim

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV TZ="Europe/Moscow"


# Install dependencies
COPY Pipfile.lock Pipfile ./


RUN pip install --no-cache-dir -U setuptools pip pipenv \
    && pipenv install --dev --deploy --system \
    && pipenv --clear

# Copy project files
COPY . .

# Make entrypoint.sh executable
RUN chmod +x ./entrypoint.sh

# Publish network port
EXPOSE 8000

# Execute script to start the application web server
ENTRYPOINT ["./entrypoint.sh"]
