#COPYRIGHT 2022
#Created by Mike Mwanga
#mikemwanga6@gmail.com
#motivation from this link

#extract the sequence id, and start and stop positions
awk -F "\t" '{OFS="\t"}{print $2,$9,$10}' results.out > hits.txt
