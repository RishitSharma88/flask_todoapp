# Use Python 3.9 slim base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]