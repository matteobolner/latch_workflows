FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main

RUN apt-get update \
    && apt-get install -y wget cmake build-essential autoconf automake libtool git pkg-config default-jre-headless openjdk-11-jdk

RUN wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.13.0+-x64-linux.tar.gz && tar -xvzf ncbi-blast-2.13.0+-x64-linux.tar.gz

RUN mkdir /root/blast_db

#COPY ncbi-blast-2.13.0+-x64-linux /root/ncbi-blast-2.13.0+-x64-linux

#setup environmental variables
ENV PATH="ncbi-blast-2.13.0+-x64-linux/bin:${PATH}"

COPY wf /root/wf

ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN  sed -i 's/latch/wf/g' flytekit.config
RUN python3 -m pip install --upgrade latch
WORKDIR /root
