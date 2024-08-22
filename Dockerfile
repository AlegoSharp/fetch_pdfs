FROM python:3.9-slim-buster

ENV TZ=Europe/Paris 

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
    tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata
# Install required Python packages

# Copy the script to the container
COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

# Set the working directory
WORKDIR /app

# Run the script
CMD ["python", "-u", "/app/App.py"]
