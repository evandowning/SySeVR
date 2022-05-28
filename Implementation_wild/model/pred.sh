#!/bin/bash

for cwe in 190 121 122 415 416; do
    time python pred.py ./model_${cwe}/BRGU \
                        "./wildcve_test/WildCVE-testset - ${cwe}.tsv" \
                        ./pred_${cwe}_train.tsv \
                        ./pred_${cwe}_test.tsv

    cat ./pred_${cwe}_train.tsv > ./pred_${cwe}_all.tsv
    cat ./pred_${cwe}_test.tsv  >> ./pred_${cwe}_all.tsv
    sort ./pred_${cwe}_all.tsv | uniq > ./pred_${cwe}_dedup.tsv

    time python roc_tsv.py ./pred_${cwe}_dedup.tsv \
                           ./pred_${cwe}_dedup.png
done
