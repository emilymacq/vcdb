#!/bin/bash

crd='157373'
file="$crd.pdf"
pdftotext $file "$crd.txt"
python processtxt.py "$crd.txt"

