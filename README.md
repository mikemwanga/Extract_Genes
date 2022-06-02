## Extract_spike_gene

This workflow extracts spike gene sequence from SARS-CoV-2 whole genome sequences.
First create a database of the whole genome sequences. Then align spike query sequence to 
blast dataase. Finally extract coordinates and trim the sequence using a python script

### Requirements
1. blast command-line tool. Download from [here](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)
2. Python 3.9.5

Execute the workflow by running the below command.

`python3 wf/__init__.py`

