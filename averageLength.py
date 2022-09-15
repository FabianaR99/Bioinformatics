#!/usr/bin/env python3

from curses import start_color
import sys

if len(sys.argv) == 1:
	print("Syntax: " + sys.argv[0] + " file.sam genomelength max_fragment_size")
	exit()

#initialize genome_change variable as a list constituted by 0 with length = genomelength
genome_length = int(sys.argv[2])
genome_change = [0]*genome_length
sum_fragment_change = [0]*genome_length
max_fragment_size = int(sys.argv[3])

sam_file = open(sys.argv[1])   #open sam file and read each line not starting with @
for line in sam_file:
	if line[0] == '@':
		continue

	fields = line.split("\t")   # makes a list of individual tab-separated fields
	if ((int(fields[1]) & 12) == 0):   # both flags unset indicates that  both segments map (8+4=12)
            if ((int(fields[8]) > 0) and (int(fields[8]) < max_fragment_size)):
                starting_mate_position = int(fields[3])
                read_length = 100
                ending_mate_position = int(fields[7]) + read_length
                # increment start position by one
                genome_change[starting_mate_position] += 1
                # decrement end position by one
                genome_change[ending_mate_position] -= 1
                #sum_fragment_change
                # increment start position by one
                sum_fragment_change[starting_mate_position] += int(fields[8]) 
                # decrement end position by one
                sum_fragment_change[ending_mate_position] -= int(fields[8]) 
sam_file.close()
	
# print genomic profile as a wiggle file
print("fixedStep chrom=genome start=1 step=1 span=1")
current_coverage = 0
coverage_sum = 0
# cicle over all positions of the genome
for position in range(genome_length):
        current_coverage += genome_change[position]
        coverage_sum += sum_fragment_change[position]
        if current_coverage > 0:
            print(coverage_sum / current_coverage)
        else:
            print(-1)