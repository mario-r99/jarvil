FROM python:3.9-alpine

WORKDIR /decision-maker
RUN apk update && apk add git
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-u", "./executor.py" ]