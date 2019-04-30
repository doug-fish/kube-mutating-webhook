FROM centos:7
RUN yum update -y && \
    yum install -y epel-release && \
    yum install -y python36 && \
    yum install -y python36-pip 
ADD *.py /
ADD *.sh /
ENV LC_ALL=en_US.utf8
ENV LANG=en_US.utf8
CMD /service.sh
