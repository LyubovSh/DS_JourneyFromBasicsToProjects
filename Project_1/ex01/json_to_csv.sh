#!/bin/sh
echo "\"id\",\"created_at\",\"name\",\"has_test\",\"alternate_url\"" > hh.csv
jq -r -f filter.jq hh.json >> hh.csv