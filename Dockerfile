# Dockerfile
# How to get the image below ?
FROM docker.jfrog.booking.com/projects/bplatform/booking-python:3.8-uwsgi
LABEL author="Jia Guo<jia.guo@booking.com>"
# set proxies
ENV HTTP_PROXY="http://webproxy:3128"
ENV HTTPS_PROXY="http://webproxy:3128"

#COPY crashmonitor-bot/requirements requirements
#COPY crashmonitor-bot/requirements.txt requirements.txt

#RUN python3 -m pip install -r requirements.txt --index-url https://jfrog.booking.com/artifactory/api/pypi/pypi/simple
#RUN python3 -m pip install bkng-infra-core booking-python-libs --index-url https://jfrog.booking.com/artifactory/api/pypi/pypi/simple
COPY crashmonitor-bot crashmonitor-bot
#COPY run_jobs.sh .
#COPY .deploy .

ENV PATH "$PATH:/opt/blue-python/3.8/bin/"

ENV PYTHONPATH "$PYTHONPATH:crashmonitor-bot"
ENV GITLAB_URL https://gitlab.booking.com
