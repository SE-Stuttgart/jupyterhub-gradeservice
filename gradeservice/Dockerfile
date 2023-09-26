FROM python:3.11-slim

RUN apt update && apt install -y --no-install-recommends \
    curl \
    ca-certificates \
    gpg \
    #pandoc \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# Install gradeservice
WORKDIR /app

COPY . .

RUN pip install . --no-cache-dir
CMD ["/bin/bash", "-c", "uvicorn gradeservice.main:app --host 0.0.0.0 --port 5000"]
