FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install curl and fwatchdog
RUN apt-get update && \
    apt-get install -y curl && \
RUN curl -sSL https://github.com/openfaas/faas/releases/download/0.13.0/fwatchdog \
    -o /usr/bin/fwatchdog && chmod +x /usr/bin/fwatchdog && \
    chmod +x /usr/bin/fwatchdog && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy app code and dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY handler.py .
COPY index.py .

# Set fprocess entrypoint
ENV fprocess="python3 main/index.py"

# Healthcheck for OpenFaaS
HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

# Run fwatchdog
CMD ["fwatchdog"]
