#! /bin/bash

for i in {0..3}
do
    for j in {0..3}
    do
	python correlation.py $i $j 0 1000 &
    done
done

exit

