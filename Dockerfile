FROM python:3.12-slim

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    build-essential \
    libsdl2-dev \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements from the main codebase
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create user and group for security
RUN groupadd -g 1003 psacln && useradd -u 10000 -g 1003 -m webadmin

# Copy the main app code
COPY . .
# COPY app.py .
# COPY constants.py .
# COPY modules ./modules
# COPY ui ./ui
# COPY simulation ./simulation

# Set file permissions
RUN chown -R webadmin:psacln /app

EXPOSE 5000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Start the Panel app
CMD ["panel", "serve", "app.py", "--address", "0.0.0.0", "--port", "5000", "--num-procs", "1", "--allow-websocket-origin=apps.kuracodez.space", "--use-xheaders", "--log-level=info", "--prefix", "/solar-system-simulation-web"]