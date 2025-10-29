#!/bin/bash
rm -f tmp.csv
find . -maxdepth 1 -name "*-*-*.csv" | while read -r filename; do
    tail -n +2 "$filename" >> tmp.csv
done
head -n 1 hh_positions.csv > result.csv
tail -n +2 tmp.csv | sort -t ',' -k2 >> result.csv