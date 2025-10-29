#!/bin/sh
curl -G -o tmp_hh.json "https://api.hh.ru/vacancies" --data-urlencode "text=$1" -d "per_page=20"
jq '.' tmp_hh.json > hh.json
rm tmp_hh.json
