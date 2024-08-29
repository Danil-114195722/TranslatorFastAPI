FROM python:3.12.2-alpine3.19

WORKDIR /root/app

# install python app requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
