# This is a sample Dockerfile you can modify to deploy your own app based on face_recognition on the GPU
# In order to run Docker in the GPU you will need to install Nvidia-Docker: https://github.com/NVIDIA/nvidia-docker

FROM nvidia/cuda:10.0-cudnn7-devel

# Install face recognition dependencies

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
    libxrender-dev

RUN pip3 install scikit-build

# Install compilers

RUN apt install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt update -y; apt install -y gcc-6 g++-6

RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 50
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-6 50

#Install dlib 

RUN git clone -b 'v19.16' --single-branch https://github.com/davisking/dlib.git
RUN mkdir -p /dlib/build

RUN cmake -H/dlib -B/dlib/build -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1
RUN cmake --build /dlib/build

RUN cd /dlib; python3.7 /dlib/setup.py install

# Install the face recognition package

RUN python3.7 -m pip install face_recognition opencv-python pyserial
