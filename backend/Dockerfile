FROM python:3.9-slim-buster

WORKDIR /app
COPY . .

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]