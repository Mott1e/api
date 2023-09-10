FROM python:3.11.2

RUN mkdir /fastapi_app

WORKDIR mkdir /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port 8000