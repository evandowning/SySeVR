#!/bin/bash

folder="/data/evan/vulchecker/labeled-dataset-master"
codeFN="dict_testcase2code_new.pkl"
pathFN="dict_flawline2filepath_new.pkl"

time python create_label.py --folder "${folder}" \
                            --outcode "${codeFN}" \
                            --outpath "${pathFN}"
