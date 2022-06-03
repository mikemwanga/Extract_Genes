"""
Explicitly extract specific gene sequences from longer genome sequences
"""

import subprocess
from pathlib import Path
from latch import small_task, workflow
from latch.types import LatchFile


@small_task
def create_database(seqfile: LatchFile) -> LatchFile:

    """
    Generate blast database.
    """

    _dir_cmd = ["mkdir", "blast_db", "Results", "Spike_gene_seq"]
    _batch_cmd = [
        "./nblast_2.13/bin/makeblastdb",
        "-in",
        seqfile,
        "-dbtype",
        "nucl",
        "-parse_seqids",
        "-out",
        "/blast_db/seq_data.fasta",
    ]

    subprocess.run(_dir_cmd)
    database = subprocess.run(_batch_cmd)
    return LatchFile(str(database), "latch:///blast_db/seq_data.fasta")


@small_task
def run_blast(query_file: LatchFile) -> LatchFile:

    """
    Run blast to generate alignment coordinates and extract gene sequences.
    """

    spike_gene_file = Path("spike_seq.fasta").resolve()

    extract_coordinates = ["sh", "scripts/extract_coordinates.sh"]

    extract_coordinates2 = ["python3", "scripts/extract.py"]

    extract_sequences = [
        "sh",
        "./scripts/read.sh",
        ">",
        "spike_seq.fasta",
    ]

    _align_cmd = [
        "./nblast_2.13/bin/blastn",
        "-query",
        query_file,
        "-db",
        "blast_db/seq_data.fasta",
        "-outfmt",
        "6",
        "-max_hsps",
        "1",
        "-out",
        spike_gene_file
    ]

    subprocess.run(_align_cmd)
    subprocess.run(extract_coordinates)
    subprocess.run(extract_coordinates2)
    subprocess.run(extract_sequences)
    return LatchFile(str(spike_gene_file), "latch:///Spike_gene_seq/spike_seq.fasta")


@workflow
def extract_spike_gene(seqfile: LatchFile, query_file: LatchFile) -> LatchFile:

    """Extract of spike gene sequence

    ## Goal
    This workflow extracts spike (glycoprotein) gene sequences from SARS-CoV-2 whole genome genome.

    ## Tools 
    1. blast command-line tool. Download from [here](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)
    2. Python 3.9.5

    ## Steps
    1. Create a database of the whole genome sequences.
    2. Align spike query sequence to blast database. Then extract coordinates and trim the sequence using a python script.

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
            multi-fasta file with SARS-CoV-2 genome sequences. Used to create blast database
            __metadata__:
                display_name: seq_file
        query_file:
            a single spike gene sequence used for mapping to blast database.
            __metadata__:
                display_name: query_sequence

    """
    create_database(seqfile=seqfile)
    return run_blast(query_file=query_file)