FROM  solr:6.2.1

MAINTAINER irrwitz <j.cyriac@gmail.com>

ENV CONDA_ENV_PATH /opt/miniconda
ENV CONDA_PY_ENV "python35"
ENV CONDA_ACTIVATE "source $CONDA_ENV_PATH/bin/activate $CONDA_PY_ENV"

USER root

# Force bash always
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Core installs
RUN apt-get update && \
    apt-get install -y git vim wget build-essential python-dev ca-certificates bzip2 libsm6 nginx && \
    apt-get clean

###############################
# START :: (mini)CONDA package manager

# Download and create
RUN wget --quiet \
    https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh && \
    bash Miniconda-latest-Linux-x86_64.sh -b -p $CONDA_ENV_PATH && \
    rm Miniconda-latest-Linux-x86_64.sh && \
    chmod -R a+rx $CONDA_ENV_PATH
ENV PATH $CONDA_ENV_PATH/bin:$PATH

RUN conda create -y -n $CONDA_PY_ENV python=3.5 pip flask requests
RUN conda install -c conda-forge uwsgi=2.0.12
RUN conda update --quiet --yes conda
RUN conda clean -y -t

RUN $CONDA_ACTIVATE

# END :: (mini)CONDA package manager
###############################


###############################
# START :: nginx conf

COPY nginx.conf /etc/nginx/nginx.con

# END :: nginx conf
###############################




# Create a user named pacs which runs the app
RUN useradd -m -s /bin/bash pacs

# Env vars
USER pacs
ENV HOME /home/pacs
ENV SHELL /bin/bash
ENV USER pacs

WORKDIR $HOME


