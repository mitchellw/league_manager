FROM ubuntu:14.04
MAINTAINER Wilson Mitchell <wilsonmitchell92@gmail.com>
RUN apt-get -qq update
RUN apt-get install -y python-dev python-setuptools supervisor git-core
RUN easy_install pip
RUN pip install virtualenv
RUN pip install uwsgi
RUN virtualenv --no-site-packages /opt/ve/league_manager
ADD . /opt/apps/league_manager
ADD .docker/supervisor.conf /opt/supervisor.conf
ADD .docker/run.sh /usr/local/bin/run
RUN /opt/ve/league_manager/bin/pip install -r /opt/apps/league_manager/requirements.txt
RUN (cd /opt/apps/league_manager && /opt/ve/league_manager/bin/python manage.py syncdb --noinput)
RUN (cd /opt/apps/league_manager && /opt/ve/league_manager/bin/python manage.py collectstatic --noinput)
EXPOSE 8000
ENTRYPOINT ["/bin/sh", "-e", "/usr/local/bin/run"]
