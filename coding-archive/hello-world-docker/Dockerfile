FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY app.py /app/app.py

EXPOSE 8080

CMD ["python", "app.py"]
