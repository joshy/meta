FROM  solr:6.2.1

MAINTAINER irrwitz <j.cyriac@gmail.com>

ENV CONDA_DIR /opt/conda
ENV CONDA_PY_ENV "python35"


USER root

# Force bash always
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Core installs
RUN apt-get update && \
    apt-get install -y git vim wget build-essential python-dev ca-certificates bzip2 libsm6 nginx && \
    apt-get clean

##############################################################
# START :: (mini)CONDA package manager
##############################################################

# Download and create
RUN wget --quiet \
    https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh && \
    bash Miniconda-latest-Linux-x86_64.sh -b -p $CONDA_DIR && \
    rm Miniconda-latest-Linux-x86_64.sh && \
    chmod -R a+rx $CONDA_DIR

ENV PATH $CONDA_DIR/bin:$PATH
RUN conda create -y -n $CONDA_PY_ENV python=3.5

# END :: (mini)CONDA package manager
##############################################################


##############################################################
# START :: nginx conf
##############################################################
RUN rm /etc/nginx/sites-enabled/default
COPY scripts/nginx.conf /etc/nginx/sites-enabled

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80 443

# END :: nginx conf
##############################################################

# Create a user named pacs which runs the app
RUN useradd -m -s /bin/bash pacs

RUN chown -R pacs:pacs $CONDA_DIR

# Env vars
USER pacs
ENV HOME /home/pacs
ENV SHELL /bin/bash
ENV USER pacs
WORKDIR $HOME

##############################################################
# START :: application
##############################################################
RUN pip install uwsgi

RUN mkdir /home/pacs/.ssh
RUN ssh-keyscan -t rsa github.com > /home/pacs/.ssh/known_hosts
RUN git clone https://github.com/irrwitz/meta.git
WORKDIR /home/pacs/meta

RUN /bin/bash -c "source activate /opt/conda/envs/python35/ && pip install -r /home/pacs/meta/requirements.txt"


ADD ./scripts/start.sh /home/pacs/start.sh
CMD ["/bin/bash", "/home/pacs/start.sh"]

# END :: application
##############################################################


