FROM python:3.11-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# Command to run the application
CMD uvicorn main:app --reload --port=8000 --host=0.0.0.0
