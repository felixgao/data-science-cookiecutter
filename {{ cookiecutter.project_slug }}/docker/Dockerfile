{%- if cookiecutter.use_nvidia_docker == 'yes' -%}
FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04 AS base
{%- else -%}
FROM ubuntu:18.04 as base
{%- endif %}

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
# Seems to speed things up
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
LABEL stage=intermediate

RUN apt-get update && apt-get install -y \
  git \
  python3.8 \
  python3-pip \
  python3.8-dev

RUN pip3 install --upgrade pip pipenv==2018.10.13 poetry

# The `dev-base` stage is used as the base for images that require
# the development dependencies. The duplication of the COPY instruction
# avoids breaking the cache for that later when the Pipfile changes 
FROM base AS dev-base
LABEL stage=intermediate
COPY Pipfile* /tmp 
RUN cd /tmp && pipenv lock -r -d > requirements.txt \
    # && pip3 install -r /tmp/requirements.txt
    && pipenv update && pipenv install --skip-lock --system  --deploy
COPY {{cookiecutter.project_slug}} /app/{{cookiecutter.project_slug}}
WORKDIR /app/{{cookiecutter.project_slug}}

# The `Test` stage runs the application unit tests, the build will fail
# if the tests fail. Note this stage name is capitalised, this is purely
# a convetion for stages which result in useful images. Think of it like
# hint that this is a public interface
FROM dev-base AS test
RUN cd /tmp && pipenv install --skip-lock  --system  --deploy --dev
COPY tests .coveragerc pytest.ini setup.cfg /app/
WORKDIR /app
RUN python3 -m pytest --black --cov={{cookiecutter.project_slug}} || true


# The `Security` stage checks the application for security vulnerabilities using the 
# Aqua MicroScanner. This requires providing a build-arg with your MicroScanner token
FROM dev-base AS security
ADD https://get.aquasec.com/microscanner /
RUN chmod +x /microscanner
RUN /microscanner NDZkM2U2MzY5YmQ4 --full-output

# `release` acts as the basis for images which will actually run the application 
FROM dev-base AS release
ARG UID
RUN useradd docker -l -u $UID -s /bin/bash -m
USER docker
ENTRYPOINT ["/bin/bash"]
