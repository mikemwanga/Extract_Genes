FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main


RUN curl -L https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.13.0+-x64-linux.tar.gz -o nblast_2.13.tar.gz && \
    tar -xvf nblast_2.13.tar.gz && mv ncbi-blast-2.13.0+ nblast_2.13


#COPY data /root/reference
#ENV BOWTIE2_INDEXES="reference"

COPY wf /root/wf

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN  sed -i 's/latch/wf/g' flytekit.config
RUN python3 -m pip install --upgrade latch
WORKDIR /root
