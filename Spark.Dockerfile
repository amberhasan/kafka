FROM bitnami/spark:latest

# Install Python dependencies
USER root
RUN apt-get update && apt-get install -y python3-pip gcc && \
    pip install --no-cache-dir spacy && \
    python3 -m spacy download en_core_web_sm && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /opt/spark/app

# Copy your Python files
COPY . /opt/spark/app
