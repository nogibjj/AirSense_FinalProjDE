# Use the official Python image as the base
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy requirements and application files to the container
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port Fastapi will run on
EXPOSE 8000

CMD ["fastapi", "dev", "app.py", "--host", "0.0.0.0"]
