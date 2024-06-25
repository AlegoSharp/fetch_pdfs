FROM python:3.9-slim-buster

# Install required packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libxslt-dev \
    libxml2-dev \
    libzip-dev \
    zip \
    unzip \
    curl \
    wget \
    ca-certificates \
    lsb-release \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Install required Python packages


# Copy the script to the container
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

# Set the working directory
WORKDIR /app

# Run the script
CMD ["python", "/app/fetch_raa_urls.py"]
