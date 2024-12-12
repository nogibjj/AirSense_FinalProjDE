# Use the official Python image as the base
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy requirements and application files to the container
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Set the entry point to run the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:create_app()", \
    "--workers", "4", "--preload"]
