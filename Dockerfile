# Use a more robust base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (sometimes needed for SysAdmin tasks/networking)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Ensure the server port is open
EXPOSE 7860

# Use a non-root user if HF Spaces requires it (optional but safer)
# RUN useradd -m appuser && chown -R appuser /app
# USER appuser

# Start the server
# Note: Ensure server/app.py starts the Flask/FastAPI app on port 7860
CMD ["python", "server/app.py"]
