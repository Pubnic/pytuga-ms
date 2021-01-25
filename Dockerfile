FROM python:3.6

RUN mkdir /code
WORKDIR /code

ENV PYTHONUNBUFFERED 1

# Install during build phase
RUN (curl -Ls https://cli.doppler.com/install.sh || wget -qO- https://cli.doppler.com/install.sh) | sh

ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/

ENTRYPOINT ["doppler", "run", "--"]
CMD python start-dev.py
