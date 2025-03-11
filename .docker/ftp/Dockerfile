FROM delfer/alpine-ftp-server
ARG USER
WORKDIR /ftp/${USER}/
RUN mkdir ./emails
RUN chmod 777 ./emails
RUN mkdir ./archive
RUN chmod 777 ./archive
VOLUME /ftp/${USER}/
