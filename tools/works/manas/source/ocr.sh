#!/bin/bash
# usage: ocr.sh <page> <outdir> <dpi> <psm>
p=$1; out=$2; dpi=$3; psm=$4
f=$(printf "%s/p%04d" $out $p)
[ -s $f.txt ] && exit 0
pdftoppm -f $p -l $p -r $dpi -gray -singlefile ${HINDI_PDF:-Hindi.pdf} $f
OMP_THREAD_LIMIT=1 tesseract $f.pgm $f -l hin --tessdata-dir ${TESSDATA:-/usr/share/tesseract-ocr/5/tessdata} --psm $psm >/dev/null 2>&1
rm -f $f.pgm
