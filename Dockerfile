# Use the official Ubuntu 20.04 image as the base image
FROM ubuntu:22.04

RUN DEBIAN_FRONTEND=noninteractive

# Update the package lists and install necessary packages
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    && apt-get clean
RUN pip install opencv-python
# Set the default Python version to Python 3
RUN ln -s /usr/bin/python3 /usr/bin/python


# Set the working directory in the container
WORKDIR /app

# Optionally, copy your application files to the container
COPY . /app

CMD ["python3","main.py"]

