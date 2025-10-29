#!/usr/bin/env python3

import cProfile
import pstats
import financial_enhanced

if __name__=="__main__":
    print(financial_enhanced.data_parser("MSFT", "Total Revenue"))
    prof = cProfile.Profile()
    prof.runcall(financial_enhanced.data_parser, "MSFT", "Gross Profit")
    with open("profiling-ncalls.txt", "w") as file:
        stats = pstats.Stats(prof, stream=file)
        stats.sort_stats("cumulative").print_stats(5)





