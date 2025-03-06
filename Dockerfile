FROM python:3.10

WORKDIR /app

RUN apt update && apt install -y unzip
RUN pip install --no-cache-dir langchain gpt4all langchain-chroma pypdf langchain_community
RUN mkdir -p /app/files

COPY mylife.zip /app/mylife.zip
COPY app.py /app/app.py
RUN unzip /app/mylife.zip -d /app/files


CMD ["python", "app.py"]