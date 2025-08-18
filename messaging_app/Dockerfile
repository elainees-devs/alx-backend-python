# Base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory inside container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev gcc \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

# Default command to run Django
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


# running the server
#docker run -p 8000:8000 messaging-api

