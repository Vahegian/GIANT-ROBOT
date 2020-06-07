# This is a sample Dockerfile you can modify to deploy your own app based on face_recognition on the GPU
# In order to run Docker in the GPU you will need to install Nvidia-Docker: https://github.com/NVIDIA/nvidia-docker

FROM nvidia/cuda:10.0-cudnn7-devel

COPY ./requirements.txt /home

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update -y  && \
    apt-get install -y build-essential python3.7 python3.7-dev python3-pip && \
    apt-get install -y git  && \
    apt-get install -y python3.7-pip && \
    apt-get update -y; apt install -y \
    git \
    cmake \
    libsm6 \
    libxext6 \
    libxrender-dev && \
    pip3 install scikit-build && \
    apt install -y software-properties-common && \
    add-apt-repository ppa:ubuntu-toolchain-r/test && \
    apt update -y; apt install -y gcc-6 g++-6 && \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 50 && \
    update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-6 50 && \
    git clone -b 'v19.16' --single-branch https://github.com/davisking/dlib.git && \
    mkdir -p /dlib/build && \
    cmake -H/dlib -B/dlib/build -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1 && \
    cmake --build /dlib/build && \
    cd /dlib; python3.7 /dlib/setup.py install && \
    python3.7 -m pip install -r /home/requirements.txt
