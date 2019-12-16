#!/bin/sh 
mkdir ./src/$1
cp ./src/template.py ./src/$1/$1.py
code ./src/$1/$1.py
touch ./src/$1/input.txt
touch ./src/$1/test.txt
code ./src/$1/test.txt
