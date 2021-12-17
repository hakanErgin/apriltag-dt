FROM jjanzic/docker-python3-opencv

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get -y install libgl1 \
    && pip install --trusted-host pypi.python.org --upgrade pip \
    && pip install opencv-contrib-python \
    && pip install pyyaml==5.4.1 \
    && pip install dt-apriltags 
