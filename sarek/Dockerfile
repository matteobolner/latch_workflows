FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main

# We'll need a Java Runtime Environment to run nextflow.
RUN apt-get update \
    && apt-get install -y default-jre-headless wget
# Here we download nextflow itself.
RUN curl -s https://get.nextflow.io | bash \
    && mv nextflow /bin/

# Here we download mamba (a more modern conda alternative) to build our
# nextflow environments.
RUN curl -L -O \
    https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Mambaforge-Linux-x86_64.sh -b \
    && rm -f Mambaforge-Linux-x86_64.sh

# Improves environment SAT solver speed. The list of versioned packages
# required to run some of these nextflow pipelines, such as nf-core/rnaseq
# here, can be difficult to resolve.
RUN /root/mambaforge/bin/conda config --set channel_priority strict

# We can store "data" files or supplementary files needed for our build, such
# as our environment file, in the `data` dir.
COPY data/environment.yml /root/

# Now we build our environment so that all downloaded packages are accessible
# to the workflow at execution time.
RUN /root/mambaforge/bin/mamba env create -f /root/environment.yml \
  && /root/mambaforge/bin/mamba clean -a

ENV PATH="/root/mambaforge/envs/nf-core-sarek-2.7.1/bin/:${PATH}"

RUN mkdir /root/sarek_output

COPY data/ /root/data/

COPY wf /root/wf

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN  sed -i 's/latch/wf/g' flytekit.config
RUN python3 -m pip install --upgrade latch
WORKDIR /root
