#!/bin/bash
for i in 10 20 30 40 50
do
	for j in `seq 1 5`
	do
		python -m src.main > $(printf 'ranking%d-%d.dat' $i $j)
	done
done
