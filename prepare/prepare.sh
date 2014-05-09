#!/bin/bash
wekadir=~/myShit/weka/weka-3-6-10/

filename=${1}

cat $filename | uniq > uniq_${filename}

cp uniq_${filename} $wekadir
