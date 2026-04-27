# OpenImuCameraCalibrator / OpenICC
# Clean & Updated Dockerfile
# Ubuntu 22.04
# Includes:
# - build-essential
# - OpenCV
# - Ceres Solver
# - pyTheiaSfM
# - Python packages
# - NodeJS (for GoPro telemetry extraction)
# - nano / vim / htop / ffmpeg
# ==========================================================

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Jakarta

# ----------------------------------------------------------
# Versions
# ----------------------------------------------------------
ENV ceresVersion=2.1.0
ENV pyTheiaVersion=69c3d37
ENV NUM_PROC=6

# ----------------------------------------------------------
# Basic tools + dependencies
# ----------------------------------------------------------
RUN apt-get update && apt-get install -y \
    tzdata \
    sudo \
    nano \
    vim \
    htop \
    wget \
    curl \
    unzip \
    pkg-config \
    software-properties-common \
    build-essential \
    checkinstall \
    cmake \
    git \
    gfortran \
    ffmpeg \
    python3 \
    python3-dev \
    python3-pip \
    python3-numpy \
    python3-opencv \
    python3-venv \
    nodejs \
    npm \
    libgtk-3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libatlas-base-dev \
    libdc1394-dev \
    libopenexr-dev \
    openexr \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libgoogle-glog-dev \
    libgflags-dev \
    libeigen3-dev \
    libopencv-dev \
    libopencv-contrib-dev \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------------
# Python packages
# ----------------------------------------------------------
RUN pip3 install --no-cache-dir \
    numpy \
    scipy \
    matplotlib \
    pandas \
    tqdm \
    natsort \
    opencv-python \
    opencv-contrib-python

# ----------------------------------------------------------
# Build CERES Solver
# ----------------------------------------------------------
WORKDIR /opt

RUN git clone https://github.com/ceres-solver/ceres-solver.git && \
    cd ceres-solver && \
    git checkout ${ceresVersion} && \
    mkdir build && cd build && \
    cmake .. \
      -DBUILD_EXAMPLES=OFF \
      -DBUILD_TESTING=OFF \
      -DCMAKE_BUILD_TYPE=Release && \
    make -j${NUM_PROC} && \
    make install && \
    ldconfig

# ----------------------------------------------------------
# Build pyTheiaSfM
# ----------------------------------------------------------
RUN git clone https://github.com/urbste/pyTheiaSfM.git && \
    cd pyTheiaSfM && \
    git checkout ${pyTheiaVersion} && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release && \
    make -j${NUM_PROC} && \
    make install && \
    ldconfig

# ----------------------------------------------------------
# Copy OpenICC source
# ----------------------------------------------------------
WORKDIR /

COPY . /home

# ----------------------------------------------------------
# Install JavaScript dependencies (FIX mp4box issue)
# ----------------------------------------------------------
RUN cd /home/javascript && \
    npm install
    
# ----------------------------------------------------------
# Build OpenICC clean
# ----------------------------------------------------------
RUN cd /home && \
    rm -rf build && \
    mkdir build && \
    cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release && \
    make -j${NUM_PROC}

# ----------------------------------------------------------
# Install python requirements if exists
# ----------------------------------------------------------
RUN if [ -f /home/requirements.txt ]; then \
    pip3 install --no-cache-dir -r /home/requirements.txt; \
    fi

# ----------------------------------------------------------
# Symlink python
# ----------------------------------------------------------
RUN ln -sf /usr/bin/python3 /usr/bin/python

# ----------------------------------------------------------
# Better matplotlib temp path
# ----------------------------------------------------------
ENV MPLCONFIGDIR=/tmp/matplotlib
RUN mkdir -p /tmp/matplotlib

# ----------------------------------------------------------
# Default working dir
# ----------------------------------------------------------
WORKDIR /home

# ----------------------------------------------------------
# Default shell
# ----------------------------------------------------------
CMD ["/bin/bash"]
