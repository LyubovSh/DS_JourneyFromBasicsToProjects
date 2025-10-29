#!/bin/sh
(head -n 1 hh.csv && tail -n +2 hh.csv | sort -t ',' -k 2 -k 1) > hh_sorted.csv