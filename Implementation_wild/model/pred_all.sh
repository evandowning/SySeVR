#!/bin/bash

for cwe in 190 121 122 415 416; do
    time python pred.py ./model_${cwe}_all/BRGU \
                        "./wildcve_test/WildCVE-testset - ${cwe}.tsv" \
                        ./pred_${cwe}_allset_train.tsv \
                        ./pred_${cwe}_allset_test.tsv

    cat ./pred_${cwe}_allset_train.tsv > ./pred_${cwe}_allset.tsv
    cat ./pred_${cwe}_allset_test.tsv  >> ./pred_${cwe}_allset.tsv
    sort ./pred_${cwe}_allset.tsv | uniq > ./pred_${cwe}_allset_dedup.tsv

    time python roc_tsv.py ./pred_${cwe}_allset_dedup.tsv \
                           ./pred_${cwe}_allset_dedup.png
done
