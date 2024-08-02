FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . . 

# 
CMD ["python3","-m","uvicorn", "app.main:app", "--port", "80", "--host", "0.0.0.0","--reload"]