FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip3 install virtualenv

COPY . /app
WORKDIR /app

RUN virtualenv venv
RUN bash -c "source venv/bin/activate"
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "wsgi.py"]
