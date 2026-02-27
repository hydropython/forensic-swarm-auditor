FROM python:3.11-slim

# Install system tools for Git analysis and UI support
RUN apt-get update && apt-get install -y \
    git \
    python3-tk \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (better for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

# Expose the port for Mission Control
EXPOSE 8001

# Start the headless display and run the app
CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & python mission_control.py"]