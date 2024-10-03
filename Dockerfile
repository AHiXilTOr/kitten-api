FROM python:3.12.6-slim

RUN apt-get update && apt-get install -y libpq-dev gcc netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /kitten_project

COPY entrypoint.sh ./

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY kitten_project/ ./

RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
