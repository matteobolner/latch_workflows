FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main
# Its easy to build binaries from source that you can later reference as
# subprocesses within your workflow.

# Or use managed library distributions through the container OS's package
# manager.
RUN apt-get update -y
RUN curl -L https://gitlab.com/mcfrith/last/-/archive/1296/last-1296.tar -o last-1296.tar && tar -xvf last-1296.tar && cd last-1296 && make

ENV PATH="/root/last-1296/bin:$PATH"

RUN mkdir /root/lastal_folder

#RUN chmod +x canu-2.2/bin/canu
#RUN ln -s canu-2.2/bin/ /usr/local/bin/canu/

#RUN ./canu

#RUN git clone https://github.com/marbl/canu.git
#RUN cd canu/src
#RUN make -j 4
#RUN mkdir /usr/local/bin/canu/
#RUN ln -s canu/bin/ /usr/local/bin/julia

#RUN python3 -m pip install flytekit

#ENV PATH="/root/miniconda3/bin:${PATH}"
#ARG PATH="/root/miniconda3/bin:${PATH}"
#RUN curl -L https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh\
#    && mkdir /root/.conda \
#    && bash Miniconda3-latest-Linux-x86_64.sh -b \
#    && rm -f Miniconda3-latest-Linux-x86_64.sh
#
##RUN conda install mamba -n base -c conda-forge
#RUN conda install -c conda-forge -c bioconda -c defaults canu
#RUN conda install -c bioconda circlator
# You can use local data to construct your workflow image.  Here we copy a
# pre-indexed reference to a path that our workflow can reference.
#COPY data/reads /root/data/reads
#COPY data/assembly /root/data/assembly
#ENV BOWTIE2_INDEXES="reference"

COPY wf /root/wf
#COPY test_data /root/test_data/

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN  sed -i 's/latch/wf/g' flytekit.config
RUN python3 -m pip install --upgrade latch
WORKDIR /root
