FROM python:3.13.5-slim

WORKDIR /pancake

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./lib /pancake/lib/
COPY main.py /pancake

CMD ["python", "main.py"]
