FROM centos:7
RUN yum update -y && \
    yum install -y epel-release && \
    yum install -y python36 && \
    yum install -y python36-pip 
ADD *.py /
ADD *.sh /
CMD /service.sh
