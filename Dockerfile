FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip3 install --upgrade pip
RUN pip3 install virtualenv

COPY . /app
WORKDIR /app

RUN virtualenv venviron
RUN bash -c "source venviron/bin/activate"

# start by pulling the python image
# FROM python:3.8

#install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt
RUN apt-get install ffmpeg libsm6 libxext6  -y

ENV PORT=8080
EXPOSE 8080

CMD ["python3", "wsgi.py" ]
