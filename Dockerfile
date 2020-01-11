FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /b2e
WORKDIR /b2e
COPY requirements.txt /b2e/
RUN pip install -r requirements.txt
COPY . /b2e/