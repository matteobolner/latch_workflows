FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main

RUN apt-get update \
    && apt-get install -y wget cmake build-essential autoconf automake libtool git pkg-config default-jre-headless openjdk-11-jdk

RUN git clone --depth=1 https://github.com/beagle-dev/beagle-lib.git && cd beagle-lib && mkdir build && cd build \
    && cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr/local/ .. && make install



RUN wget https://github.com/beast-dev/beast-mcmc/releases/download/v1.10.4/BEASTv1.10.4.tgz && tar -xvzf BEASTv1.10.4.tgz
RUN mkdir /root/beast_output
#setup environmental variables
ENV PATH="/root/BEASTv1.10.4/bin/:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
ENV PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"

COPY wf /root/wf

ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN  sed -i 's/latch/wf/g' flytekit.config
RUN python3 -m pip install --upgrade latch
WORKDIR /root
