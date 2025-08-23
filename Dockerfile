FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    bash \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . .

# Expose port 8000 for Django server
EXPOSE 8000

# Run migrations and start the Django development server
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
