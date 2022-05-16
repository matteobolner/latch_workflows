FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/wf-base:fbe8-main
# Its easy to build binaries from source that you can later reference as
# subprocesses within your workflow.

# Or use managed library distributions through the container OS's package
# manager.
RUN apt-get update -y &&\
    apt-get install -y autoconf curl bwa samtools python3 python3-pip bowtie2 mummer canu prodigal

#RUN curl -L https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.4/bowtie2-2.4.4-linux-x86_64.zip/download -o bowtie2-2.4.4.zip &&\
#    unzip bowtie2-2.4.4.zip &&\
#    mv bowtie2-2.4.4-linux-x86_64 bowtie2

#RUN curl -L https://sourceforge.net/projects/mummer/files/mummer/3.23/MUMmer3.23.tar.gz/download -o MUMmer3.23.tar.gz &&\
#    tar -xvf MUMmer3.23.tar.gz &&\
#    mv MUMmer3.23.tar.gz mummer3

#RUN curl -L https://github.com/hyattpd/Prodigal/releases/download/v2.6.3/prodigal.linux -o prodigal

#RUN curl -L https://github.com/marbl/canu/releases/download/v2.2/canu-2.2.linux-amd64.tar.xz -o canu-2.2.linux.tar.xz &&\
#    tar -xJf canu-2.2.linux.tar.xz

RUN curl -L https://github.com/ablab/spades/releases/download/v3.15.4/SPAdes-3.15.4-Linux.tar.gz -o SPAdes-3.15.4-Linux.tar.gz &&\
    tar -xvf SPAdes-3.15.4-Linux.tar.gz

ENV PATH="/root/SPAdes-3.15.4-Linux/bin:$PATH"

#RUN mkdir /usr/local/bin/canu/

#RUN chmod +x canu-2.2/bin/canu
#RUN ln -s canu-2.2/bin/ /usr/local/bin/canu/

RUN python3 -m pip install circlator


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
