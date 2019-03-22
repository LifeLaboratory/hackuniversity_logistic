FROM python:3

WORKDIR /usr/src/auth

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "./main.py" ]