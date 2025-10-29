#!/bin/bash

echo "\"name\"" > levels.csv

tail -n +2 hh_sorted.csv | while IFS= read -r line
do
    result=$(echo "$line" | grep -io "Junior\|Middle\|Senior" | tr '\n' '/' | sed 's/\/$//')
    
    if [ -z "$result" ]; then
        result="-"
    fi
    echo "$result" >> levels.csv
done


paste -d ',' <(cut -d'"' -f1,2,3,4,5 hh_sorted.csv) levels.csv <(cut -d'"' -f7,8,9,10,11 hh_sorted.csv) > tmp.csv
paste -d ',' <(cut -d',' -f1,2,4,6,7 tmp.csv) > hh_positions.csv
rm levels.csv
rm tmp.csv