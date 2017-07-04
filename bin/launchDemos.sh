#!/usr/bin/env bash
echo "###################################"
echo "### LAUNCHING DEMO APPLICATIONS ###"
echo "###################################"
echo ""
echo "*******************************"
echo "*** Summer application test ***"
echo "*******************************"
echo ""

runcompss -g run_demo.py summer

#echo ""
#echo "*******************************"
#echo "*** Other application test ***"
#echo "*******************************"
#echo ""
#
#runcompss -g other.py args

echo ""
echo "###################################"
echo "### DEMO APPLICATIONS FINISHED  ###"
echo "###################################"
echo ""

echo "Now you can run the skeleton: runcompss -g MYAPP.py file1 file2 metadata.json outputFile2"
