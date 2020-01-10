FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /B2E
WORKDIR /B2E
COPY requirements.txt /B2E/
RUN pip install -r requirements.txt
COPY . /B2E/