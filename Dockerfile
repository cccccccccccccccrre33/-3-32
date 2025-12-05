FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install numpy==1.25.2
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
