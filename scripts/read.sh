#!/bin/bash
#Script to extract SARS-Cov-2 genome using blast.
#COPYRIGHT 2022
#Created by Mike Mwanga
#mikemwanga6@gmail.com
#motivation from this link
#https://www.biostars.org/p/433926/


while read id start stop; do
	./executables/nblast_2.13/bin/blastdbcmd -db ./blast_db/seq_data.fasta -entry $id -range $start-$stop
done < ./Results/sequence_coordinates.txt > Spike_gene_seq/spike_gene.fasta
