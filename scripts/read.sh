#!/bin/bash
#Script to extract SARS-Cov-2 genome using blast.
#COPYRIGHT 2022
#Created by Mike Mwanga
#mikemwanga6@gmail.com
#motivation from this link
#https://www.biostars.org/p/433926/


while read id start stop; do
	./nblast_2.13/bin/blastdbcmd -db database.fasta -entry $id -range $start-$stop
done < sequence_coordinates.txt > spike_gene.fasta
