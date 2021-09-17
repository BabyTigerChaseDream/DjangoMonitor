#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "create_version.sh"
# PLEASE DO NOT EDIT IT DIRECTLY.
#
### default Dockerfile :
# https://gitlab.booking.com/bplatform/base-images/-/blob/fe034afad5d6dfe05126b41ecd05038764ecb3c4/booking-python/base/3.8/Dockerfile
FROM docker.artifactory.booking.com/projects/bplatform/booking-python:3.7

#ENV HTTP_PROXY "http://webproxy:3128/"
#ENV HTTPS_PROXY "http://webproxy:3128/"
#ENV SECRETS_FOLDER "/var/run/secrets/booking.com"

# Install package 
#RUN python3 -m pip install bkng-infra-db --index-url https://jfrog.booking.com/artifactory/api/pypi/pypi/simple
RUN python3 -m pip install bkng-infra-core bkng-infra-db booking-python-libs --index-url https://jfrog.booking.com/artifactory/api/pypi/pypi/simple
RUN python3 -m pip install flask
RUN python3 -m pip install schedule

#CMD ["python3 --version","python3 -m pip list | grep bkng","ll /etc/bookings"]

WORKDIR /workspace
COPY . /workspace

RUN python3 -m pip install -r requirements.txt
RUN yum install -y vim
RUN chmod 777 run.sh
EXPOSE 8000
#ENTRYPOINT [ "python" ]
CMD ["/bin/sh","run.sh"]
#CMD [ "app.py" ,"python","./FirebaseCrashH2/src/utils.py &"]
#CMD [ "python","manage.py", runserver 0.0.0.0:8000"]
