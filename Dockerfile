ARG BASE_IMAGE=python:3.13
FROM $BASE_IMAGE

# system update & package install
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    openssl libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .
WORKDIR .

# pip & requirements
RUN pip install prometheus-client starlette-prometheus
RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install -r requirements.txt

# Configuration
EXPOSE 8000

# Execute
CMD ["python", "main.py"]
