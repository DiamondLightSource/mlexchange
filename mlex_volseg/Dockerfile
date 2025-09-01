# Use a CUDA-enabled base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Copy requirements file
COPY ./dist/volume_segmantics-0.3.2-py3-none-any.whl /dist/volume_segmantics-0.3.2-py3-none-any.whl

# Set up environment and install system dependencies
RUN apt-get update && apt-get install -y \
        curl git bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 python3-pip nano libgl1 lsof gnuplot\
    && pip install /dist/volume_segmantics-0.3.2-py3-none-any.whl imageio zarr scikit-image\
    && rm -rf /var/lib/apt/lists/* /root/.cache/pip\
    && apt-get clean

# Copy source code and configuration files
COPY ./src/volseg_interface.py /volseg_interface.py


COPY ./src/generate_volseg_settings.py /generate_volseg_settings.py
COPY ./config/volseg-settings/ /volseg-settings
COPY ./to-predict/ /to-predict

COPY ./run.sh /run.sh
RUN chmod +x /run.sh

# Keep shell alive for interactive use
CMD ["bash"]

