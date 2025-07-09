# Use Ubuntu as base image for better Vala/libpeas support
FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set UTF-8 encoding for proper Unicode support
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Build tools
    build-essential \
    make \
    pkg-config \
    # Vala compiler and development libraries
    valac \
    libpeas-dev \
    libglib2.0-dev \
    gobject-introspection \
    libgirepository1.0-dev \
    gir1.2-peas-1.0 \
    # Runtime libraries
    libglib2.0-0 \
    libpeas-1.0-0 \
    # Python and pip
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    # AI/ML dependencies
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    gfortran \
    # Audio support for speech recognition
    portaudio19-dev \
    python3-pyaudio \
    alsa-utils \
    # Additional utilities
    git \
    wget \
    curl \
    # UTF-8 locale support
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen en_US.UTF-8

# Set Python3 as default python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies (AI libraries can be large, so we increase timeout)
RUN pip3 install --timeout 1000 -r requirements.txt

# Copy source code
COPY . .

# Create bin directory structure
RUN mkdir -p bin/plugins

# Build the application
RUN make clean && make all

# Install plugins
RUN make install

# Set environment variables for runtime
ENV LD_LIBRARY_PATH="/app/bin"
ENV GI_TYPELIB_PATH="/app/bin"
ENV PATH="/app/bin:$PATH"

# Set working directory to bin for execution
WORKDIR /app/bin

# Make sarah executable available
RUN ln -s /app/bin/sarah /usr/local/bin/sarah

# Default command
CMD ["sarah"]

# Add metadata
LABEL maintainer="Sarah Assistant"
LABEL description="Sarah Terminal Assistant - Your helpful command-line companion"
LABEL version="1.0" 