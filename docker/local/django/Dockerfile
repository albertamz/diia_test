FROM python:3.11

# to see logs in real-time
ENV PYTHONUNBUFFERED=1 \
    # prevent creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip vars
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    # directory for the project
    PROJECT_DIR="/code"

RUN apt-get update && \
    apt-get install -qy \
        cmake \
        build-essential \
        libhiredis-dev \
        libpq-dev


RUN mkdir /$PROJECT_DIR

# set work directory
WORKDIR $PROJECT_DIR
ADD . $PROJECT_DIR

# update pip
RUN pip install --upgrade pip setuptools
ADD ./requirements.txt ./
ADD ./docker/local/django/start.sh /start
RUN chmod +x /start


#RUN mkdir logs
RUN pip install -r requirements.txt
