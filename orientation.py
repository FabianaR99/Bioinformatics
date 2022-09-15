#!/usr/bin/env python3

import sys

if len(sys.argv) == 1:
	print("Syntax: " + sys.argv[0] + " file.sam genomelength max_fragment_size orientation")
	exit()

#initialize genome_change variable as a list constituted by 0 with length = genomelength
genome_length = int(sys.argv[2])
genome_change_forward=  [0]*genome_length
max_fragment_size = int(sys.argv[3])
orientation =  int(sys.argv[4])

sam_file = open(sys.argv[1])   #open sam file and read each line not starting with @
for line in sam_file:
	if line[0] == '@':
		continue

	fields = line.split("\t")   # makes a list of individual tab-separated fields
	if ((int(fields[1]) )& 12 == 0):   # both flags unset indicates that  both segments map (8+4=12)
            if ((int(fields[8]) > 0) and (int(fields[8]) < max_fragment_size)):
                if (int(fields[1]) & 48 == orientation): #16 + 32 = 48
                    starting_mate_position = int(fields[3])
                    mate_length = 100
                    # increment start position by one
                    genome_change_forward[starting_mate_position] += 1
                    # decrement end position by one
                    genome_change_forward[starting_mate_position + 2 * mate_length] -= 1
sam_file.close()
	
# print genomic profile as a wiggle file
print("fixedStep chrom=genome start=1 step=1 span=1")
current_coverage = 0
# cicle over all positions of the genome
for position in range(genome_length):
	current_coverage += genome_change_forward[position]
	print(current_coverage)