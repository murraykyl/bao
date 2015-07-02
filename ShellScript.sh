#!
# This script will run the programs necessary to complete our
# correlation function from the BlueHive computer system
# Research with Professor Regina Demina
# University of Rochester Physics and Astronomy

# Set up a directory to house all stdouts
mkdir BAOHistograms

# Install ROOT
#gzip -dc root_6.04.00.source.tar.gz | tar -xf -
#cd root
#make -j 4
#source bin/thisroot.csh
#root
#q
# This should have accounted for Python Bindings

# Run Programs
python corrHistogram.py

mv *.pdf BAOHistograms















