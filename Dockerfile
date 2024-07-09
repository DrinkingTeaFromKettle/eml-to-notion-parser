FROM delfer/alpine-ftp-server
WORKDIR /ftp/admin/
RUN mkdir ./emails
RUN chmod 777 ./emails
RUN mkdir ./archive
RUN chmod 777 ./archive
VOLUME /ftp/admin/
