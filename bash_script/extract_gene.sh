#!/bin/bash
#SCRIPT TO EXTRACT SPECIFIC GENE SEQUENCES FROM FULL GENOME SEQUENCES
#REQUIREMENTS - INSTALL blast TOOL PREFERABLY USING CONDA
#CAN ALSO MODULE LOAD THE BLAST MODULE IN SERVER
#COPYRIGHT 2023


#QUICK START
# '''
# Ensure blast is installed preferably using conda.
# Alternatively use blast module if already installed in hpc
# '''

#STEPS
#1.pass the mega fasta file which will form the database
#2. pass the query sequence - gene sequence
#3. check output in file named sequence_out.fas

# USAGE bash chop.sh dabatasefile gene_file
usage="sh extract_gene.sh mega_fasta.seq.fasta gene_sequence.fasta"

outfile='sequence_out.fas'
dbname='database' #set databasename
touch blastresults.out
infile='hits.txt'

#set arguments to be passed
database_file=$1
gene_file=$2
#check that two arguments are passed, else exit
if [ $# -eq 2 ]
    then
    #create database of your seqeunces
    echo 1. Creating blast database.
    makeblastdb -in $database_file -dbtype nucl -parse_seqids -out $dbname > makeblastn.log
    echo ---- Creating blast database complete.
    # #RUN BLAST QUERY ON THE DATABASE

    echo 2. Running blast.......
    blastn -query $gene_file -db $dbname -outfmt 6 -max_hsps 1 -out blastresults.out

    echo ---- blastn complete
    awk -F "\t" '{OFS="\t"}{print $2,$9,$10}' blastresults.out > hits.txt


    echo 3. Extracting query sequences
    while read -r ID start stop
    do
        blastdbcmd -db "$dbname" -entry "$ID" -range "$start-$stop"

    done < "$infile" > "$outfile"

    rm hits.txt blastresults.out

    echo 4. Analysis complete.
    echo ---- Voila!

else
    echo "No file passed. Check usage of file"
    echo $usage
    exit 1
fi




