#!/bin/bash
file=hh_positions.csv

tail -n +2 "$file" | while IFS= read -r line
do
    date=$(echo "$line" | grep -E -io '[0-9]{4}-[0-9]{2}-[0-9]{2}')

    if [ -n "$date" ]; then
        if [ ! -f "$date.csv" ]; then
            head -n 1 "$file" > "$date.csv"
        fi
        echo "$line" >> "$date.csv"
    fi   
done


