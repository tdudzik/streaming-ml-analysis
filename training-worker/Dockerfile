FROM python:3.11

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENTRYPOINT ["python", "main.py"]
