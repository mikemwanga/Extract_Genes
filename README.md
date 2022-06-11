## Extract_spike_gene

This workflow extracts spike (glycoprotein) gene portions from SARS-CoV-2 whole genome sequences.
Same principle can be applied while extracting gene sequences from longer genomes.

## Tools 
1. blast command-line tool. Download from [here](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)
2. Python 3.9.5

## Test Data
The test dataset contains a set of SARS-CoV-2 complete genome sequences downloaded from [GISAID](https://www.gisaid.org) database.
This multi-fasta file is referred as seqfile in the subsequent steps. The query file contains a single fasta sequence - in here the 
surface glycoprotein gene sequence from SARS-CoV-2 [Wuhan strain](https://www.ncbi.nlm.nih.gov/nuccore/NC_045512.2)

## Steps
1. Create a database of the whole genome sequences.
2. Align spike query sequence to blast database. Use mapping coordinates to extract the target gene sequences from database.

Link to the code [here](https://github.com/mikemwanga/wf-sars_cov_spike_gene/blob/main/wf/__init__.py)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
