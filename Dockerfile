FROM ubuntu:22.04
WORKDIR /usr/app/src
COPY requirements.txt ./
RUN apt update
RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
RUN apt install -y libgl1-mesa-glx
RUN apt install -y python3-pip
RUN pip install -r requirements.txt
COPY . .
CMD ["echo ${CONTENT_URL}"]
CMD [ "python3", "-u", "./main.py"]