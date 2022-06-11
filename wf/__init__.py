"""
Explicitly extract specific gene sequences from longer genome sequences. Example glycoprotein sequence from SARS-CoV-2 whole genome.
"""
from subprocess import Popen
import subprocess
from pathlib import Path
from latch import small_task, workflow
from latch.types import LatchFile
import pandas as pd

@large_task

def create_database(seqfile: LatchFile, query_file:LatchFile) -> LatchFile:
    """
    Generate blast database, map query to database and extract target gene sequence.
    """
    _batch_cmd = [
        "./nblast_2.13/bin/makeblastdb",
        "-in",
        seqfile,
        "-dbtype",
        "nucl",
        "-parse_seqids",
        "-out",
        "database",
    ]
    subprocess.run(_batch_cmd)

    #create output files
    _blast_results = ["touch", "blastresults.out", "coordinates.txt", "spike_gene.fasta",
    			"hits.txt"]
    blast_output = Path("blastresults.out")
    coordinates_file = Path("coordinates.txt")
    spike_gene = Path("spike_gene.fasta")
    
    #run blast of query to database
    _align_cmd = [
        "./nblast_2.13/bin/blastn",
        "-query",
        query_file,
        "-db",
        "database",
        "-outfmt",
        "6",
        "-max_hsps",
        "1",
        "-out",
        blast_output
    ]
    subprocess.run(_blast_results)
    subprocess.run(_align_cmd)
    
    #extract sequence IDs, and start and stop coordinates
    _extract_cmd = """
    awk -F "\t" '{OFS="\t"}{print $2,$9,$10}' blastresults.out > hits.txt
    """
    Popen(_extract_cmd, shell=True,stdout=subprocess.PIPE).communicate()

    hits_data = pd.read_table("hits.txt", sep = "\t", usecols=[0,1,2], names = ["ID", "start","stop"])   
    hits_data["length"] =  hits_data.apply(lambda x: x.stop - x.start, axis=1)
    hits = hits_data[hits_data["length"] > 3000]  
    hits = hits.drop("length", axis=1)
    hits.to_csv(coordinates_file,sep = "\t", header=False, index=False)
    
    #extract glycoprotein gene sequences based on the determined coordinates
    _get_seq = """
    while read id start stop; do
		./nblast_2.13/bin/blastdbcmd -db database -entry $id -range $start-$stop
	done < coordinates.txt > spike_gene.fasta
    """
    Popen(_get_seq, shell=True,stdout=subprocess.PIPE).communicate()
    
    return LatchFile(str(spike_gene), f"latch:///spike_gene.fasta") #return file with spike gene sequences

@workflow
def extract_spike_gene(seqfile: LatchFile, query_file: LatchFile) -> LatchFile:

    """Extract of spike gene sequence

    ## Goal
    This workflow extracts spike (glycoprotein) gene sequences from SARS-CoV-2 whole genome genome.
    Same principle can be applied while extracting gene sequences from longer genomes.

    ## Tools 
    1. blast command-line tool. Download from [here](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)
    2. Python 3.9.5

    ## Test Data
    The test dataset contains a set of SARS-CoV-2 complete genome sequences downloaded from [GISAID](https://www.gisaid.org) database.
    This multi-fasta file is referred as seqfile in the subsequent steps. The query file contains a single fasta sequence. In here the 
    surface glycoprotein gene sequence from SARS-CoV-2 [Wuhan strain](https://www.ncbi.nlm.nih.gov/nuccore/NC_045512.2)

    ## Steps
    1. Create a database of the whole genome sequences.
    2. Align spike query sequence to blast database. Use mapping coordinates to extract the target gene sequences from database.

    Link to the code [here](https://github.com/mikemwanga/wf-sars_cov_spike_gene/blob/main/wf/__init__.py)

    __metadata__:
        display_name: extract_spike_gene
        author:
            name: Mike Mwanga
            email: mikemwanga6@gmail.com
            github: https://github.com/mikemwanga/wf-sars_cov_spike_gene
            repository: 
            license:
                id: MIT

    Args:
        seqfile:
            multi-fasta file with SARS-CoV-2 genome sequences. Used to create blast database.
            __metadata__:
                display_name: seqfile

        query_file:
            a single spike gene sequence used for mapping to blast database.
            __metadata__:
                display_name: query_sequence

    """
    return create_database(seqfile=seqfile, query_file=query_file)