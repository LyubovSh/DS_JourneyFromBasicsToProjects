#!/bin/bash
cut -d ',' -f3 hh_positions.csv | tail -n +2 | uniq > tmp.csv
echo "name,count" > hh_uniq_positions.csv
echo "Junior, $(grep -c -i 'Junior' tmp.csv)" > hh_uniq_positions.csv
echo "Middle, $(grep -c -i 'Middle' tmp.csv)" >> hh_uniq_positions.csv
echo "Senior, $(grep -c -i 'Senior' tmp.csv)" >> hh_uniq_positions.csv
sort -t ',' -k 2 -r hh_uniq_positions.csv
rm tmp.csv
