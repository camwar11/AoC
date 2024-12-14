#!/bin/sh 
day="day$2"
mkdir ./src/$1/$2
cp ./src/template.py ./src/$1/$2/$day.py
# code ./src/$1/$2/$day.py
# touch ./src/$1/$2/input.txt
# touch ./src/$1/$2/test.txt
# code ./src/$1/$2/test.txt
