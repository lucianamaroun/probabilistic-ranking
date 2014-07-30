#!/bin/bash
for i in 429 857 1286 1715 2144 2572 3001 3430 3858 4287  
do
	for j in `seq 1 5`
	do
		python -m src.main -t 10 $i 
	done
done
