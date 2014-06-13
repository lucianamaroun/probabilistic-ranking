#!/bin/bash
for i in 60 70 80 90 100 
do
	for j in `seq 1 5`
	do
		python -m src.main $i > $(printf 'ranking%d-%d.dat' $i $j)
	done
done
