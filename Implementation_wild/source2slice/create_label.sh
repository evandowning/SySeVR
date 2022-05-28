#!/bin/bash

run() {
    id="$1"
    folder="/home/evan/labeled-dataset-master/CWE${id}"
    codeFN="dict_testcase2code_new_${id}.pkl"
    pathFN="dict_flawline2filepath_new_${id}.pkl"
    vulnFN="label_vec_type_new_${id}.pkl"

    time python create_label_single.py --folder "${folder}" \
                                       --outcode "${codeFN}" \
                                       --outpath "${pathFN}" \
                                       --outvuln "${vulnFN}"
}

for id in 121 122 190 191 415 416; do
    run "${id}"
done
