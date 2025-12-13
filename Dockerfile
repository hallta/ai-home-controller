FROM debian:trixie-slim

RUN apt-get update
RUN apt-get install -y \
        binutils \
        curl \
        xz-utils \
        git \
        tar \
        file \
        wget \
        procps \
        net-tools \
        vim \
        screen \
        xz-utils \
        iputils-ping \
        sudo \
        dnsutils

#COPY load/*csv /tmp/

#COPY bootstrap.sh /bin/bootstrap_container
#COPY pg_hba.conf /tmp/pg_hba.conf
#COPY load.sql /tmp/load.sql

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Create a new user 'trevor' with home directory at
# /home/trevor and default shell /bin/bash
RUN useradd -m -d /home/trevor -s /bin/bash trevor
RUN echo 'trevor ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

#RUN chmod +x /bin/bootstrap_container
#CMD bash -C '/bin/bootstrap_container';'bash'
