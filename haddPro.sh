#! /bin/bash

for i in {1..4}
do
    for j in {1..4}
    do
	python correlation.py $i $j &
    done
done

exit

