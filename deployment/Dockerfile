FROM python:3.11

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install gcc libc-dev g++ libffi-dev libxml2 libffi-dev libpq-dev unixodbc-dev -y

ARG WDIR=/home/application

WORKDIR $WDIR

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

ENTRYPOINT ["python", "-m", "uvicorn", "src.api.main:application", "--host", "0.0.0.0", "--port", "80"]
