from pathlib import Path
from latch import small_task, workflow
from latch.types import LatchFile
import subprocess


@small_task
def create_database(seqfile: LatchFile) -> LatchFile:
    
    _dir_cmd = ['mkdir', 'blast_db', 'Results', "Spike_gene_seq"]
    _batch_cmd = [
        './executables/nblast_2.13/bin/makeblastdb',
        '-in', seqfile,
        '-dbtype',
        'nucl',
		'-parse_seqids',
        '-out', './blast_db/seq_data.fasta' ]

    subprocess.run(_dir_cmd)
    database = subprocess.run(_batch_cmd)
    return LatchFile(str(database), "latch:///blast_db/seq_data.fasta")

@small_task
def run_blast(query_file: LatchFile) -> LatchFile:

   
    coordinates_file = Path("./Results/results.out").resolve()

    extract_coordinates = [
        "sh", "./scripts/extract_coordinates.sh"]
    
    extract_coordinates2 = [ 
        "python3", "./scripts/extract.py"]

    extract_sequences = [ 
        "sh", "./scripts/read.sh", ">", "./Spike_gene_seq/spike_seq.fasta" ]
    

    _align_cmd = [
        './executables/nblast_2.13/bin/blastn',
        '-query', query_file,
		'-db', './blast_db/seq_data.fasta',
		'-outfmt', '6',
		'-max_hsps','1',
        '-out', 
        str(coordinates_file) ]
    
    subprocess.run(_align_cmd)
    subprocess.run(extract_coordinates)
    subprocess.run(extract_coordinates2)
    subprocess.run(extract_sequences)
    return LatchFile(str(coordinates_file), "latch:///Results/results.out")

############

@workflow
def run_sars_spike(seqfile: LatchFile) -> LatchFile:
    """ Description
    ## extract_spike_gene

    This workflow extracts spike gene seqeunce from SARS-CoV-2 whole genome genome
    First create a database of the whole genome seqeunces. Align spike query sequence to 
    blast dataase. Then extract coordinates and trim the sequence using a python script

    __metadata__:
        display_name: extract SARS-CoV-2 gene sequence
        author:
            name: Mike Mwanga
            email: mikemwanga6@gmail.com
            github:mikemwanga
            repository:wf/sars_cov_spike_gene
            license:
            id:MIT

    Args:
        seqfile:
            multi-fasta file with SARS-CoV-2 genome sequences. Used to create blast database 
            __metadata__:
                display_name: seq_file
        query_file:
            a single spike gene sequence used for mapping to blast database. 
            __metadata__:
                display_names: query_sequence

    """
    
    create_database(seqfile=seqfile)

    return run_blast(query_file=LatchFile("./data/query_seq.fasta"))

run_sars_spike(seqfile=LatchFile("./data/seq_data.fasta"))