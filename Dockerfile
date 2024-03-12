# Use the specified Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install curl for the health check
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy the requirements and install them
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the rest of the application
COPY . .

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Expose the desired port
EXPOSE 8080

# Add a health check
HEALTHCHECK CMD curl --fail http://localhost:8080/_stcore/health || exit 1

# Define the command to start the app
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]


