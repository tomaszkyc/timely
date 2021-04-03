FROM python:3.8

# get python dependencies
WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


# install npm and install dependencies
RUN apt-get update -y && \
    apt-get install -y npm && \
    apt-get install -y default-mysql-client

CMD ["npm install"]


# prepare js / css files
CMD ["python", "release_dev.py"]


# set environment variables for flask app
ENV FLASK_ENV=development
ENV FLASK_APP=main.py
ENV APP_SETTINGS=development
ENV DATABASE_URL=mysql://user:password@db:3306/db


# before flask app execution check if db is ok
RUN chmod 777 init-and-wait-for-db.sh
