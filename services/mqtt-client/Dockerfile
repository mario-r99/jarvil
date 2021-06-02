FROM python:3.9-alpine

WORKDIR /client

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "./client.py" ]