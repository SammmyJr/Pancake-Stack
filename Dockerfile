FROM python:3.13.5

WORKDIR /app

ADD main.py /app
ADD .env /app

RUN apt-get update -y
RUN curl -fsSL https://ollama.com/install.sh | sh

COPY requirements.txt requirements.txt
COPY ./lib /app/lib/

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]
