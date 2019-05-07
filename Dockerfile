FROM centos:7
RUN yum update -y && \
    yum install -y epel-release && \
    yum install -y python36 && \
    yum install -y python36-pip && \
    pip3 install --user Flask && \
    pip3 install jsonpatch
ADD *.py /
ADD *.sh /
ENV LC_ALL=en_US.utf8
ENV LANG=en_US.utf8
ENV FLASK_APP=service.py
CMD /service.sh
