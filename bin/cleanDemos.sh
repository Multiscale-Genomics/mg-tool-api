#!/usr/bin/env bash
echo "################################"
echo "### CLEANING TEMPORARY FILES ###"
echo "################################"
echo ""

find . -name "*.pyc" -type f -delete

rm file*
rm partial.out
rm outputFile
rm outputFile2
