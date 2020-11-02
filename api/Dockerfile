FROM python:3.9

MAINTAINER Jerome <jkpaddick@gmail.com>

COPY . /usr/src/api
WORKDIR /usr/src/api

RUN pip install -r requirements.txt

# for running with gunicorn
 ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]

# for testing (has live reloading)
#ENTRYPOINT ["python", "/usr/src/api/server.py"]