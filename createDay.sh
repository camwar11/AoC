#!/bin/sh 
mkdir ./src/$1/$2
cp ./src/template.py ./src/$1/$2/$2.py
code ./src/$1/$2/$2.py
touch ./src/$1/$2/input.txt
touch ./src/$1/$2/test.txt
code ./src/$1/$2/test.txt
