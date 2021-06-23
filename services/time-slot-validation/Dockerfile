FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libzbar0 \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "./app.py" ]