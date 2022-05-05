#!/bin/bash

rm -rf ./cfg_db/; mkdir ./cfg_db/
time python get_cfg_relation.py

rm -rf ./pdg_db/; mkdir ./pdg_db/
time python complete_PDG.py

rm -rf ./dict_call2cfgNodeID_funcID/; mkdir ./dict_call2cfgNodeID_funcID/
time python access_db_operate.py

time python points_get.py

rm -rf ./C/; mkdir -p ./C/test_data/4/
rm -rf ./pdg_db/testCode/; mkdir -p ./pdg_db/testCode/
time python extract_df.py > extract_df_stdout.txt

time python make_label.py

rm -rf ./slices/; mkdir ./slices/; find ./C/ -type f -name '*.txt' -exec cp {} slices/ \;
rm -rf ./label_source/; mkdir ./label_source/; find ./C/ -type f -name '*.pkl' -exec cp {} label_source/ \;
rm -rf ./slice_label/; mkdir ./slice_label/
time python data_preprocess.py
