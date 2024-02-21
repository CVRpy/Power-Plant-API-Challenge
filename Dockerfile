# Use the official Python image as a base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install Flask and other dependencies
RUN pip install -r requirements.txt

# Copy the Flask application code to the container
COPY . .

# Expose port 8888 to the outside world
EXPOSE 8888

# Command to run the Flask application
CMD ["python", "app.py"]
