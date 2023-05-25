FROM docker.io/condaforge/mambaforge@sha256:a119fe148b8a276397cb7423797f8ee82670e64b071dc39c918b6c3513bd0174

RUN bin/bash

## Creating the new conda environment with the desired packages using mamba
WORKDIR /opt
COPY environment.yml .
RUN mamba env create -f environment.yml
RUN echo "conda activate upwork_scrapper" >> ~/.bashrc


# Install base utilities
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y build-essential  && \
    apt-get install -yq curl wget jq vim xvfb unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Install Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get update
RUN apt-get -y install ./google-chrome-stable_current_amd64.deb

# Copy all the relevant Files
COPY slack_bot/ /opt/upwork_slackbot/slack_bot/
COPY upwork_bot/ /opt/upwork_slackbot/upwork_bot/
COPY config.py /opt/upwork_slackbot/config.py
COPY main.py /opt/upwork_slackbot/main.py

ENTRYPOINT ["/opt/conda/envs/upwork_scrapper/bin/python","-u", "/opt/upwork_slackbot/main.py"]

