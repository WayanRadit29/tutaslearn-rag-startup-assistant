FROM python:3.12-slim

WORKDIR /app

# Install build dependencies for sentence-transformers (optional, for faster embedding)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY build_index.py .
COPY query_engine.py .
COPY app.py .
COPY static/ ./static/

# Copy data and storage (vector index must be built first)
COPY data/ ./data/
COPY storage/ ./storage/

# Create logs directory
RUN mkdir -p /app/data/logs

EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
