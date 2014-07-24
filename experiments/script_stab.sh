#!/bin/bash
for i in 1 2 5 10 22 46 100 215 464 1000 
do
	for j in `seq 1 3`
	do
		python -m src.main -t $i > $(printf 'ranking%d-%d.dat' $i $j)
	done
done
