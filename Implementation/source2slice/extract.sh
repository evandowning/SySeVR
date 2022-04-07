#!/bin/bash

# Takes 12 minutes for CWE416
rm -rf ./cfg_db/; mkdir ./cfg_db/
time python get_cfg_relation.py

# Takes 45 minutes for CWE416
rm -rf ./pdg_db/; mkdir ./pdg_db/
time python complete_PDG.py

# Takes 1 minute for CWE416
rm -rf ./dict_call2cfgNodeID_funcID/; mkdir ./dict_call2cfgNodeID_funcID/
time python access_db_operate.py

# Takes 16 minutes for CWE416
time python points_get.py

# Takes 5 minutes for CWE416
rm -rf ./C/; mkdir -p ./C/test_data/4/
rm -rf ./pdg_db/testCode/; mkdir -p ./pdg_db/testCode/
time python extract_df.py

# Takes 17 seconds for CWE416
time python make_label.py

# Takes about 2 seconds for CWE416
rm -rf ./slices/; mkdir ./slices/; find ./C/ -type f -name '*.txt' -exec cp {} slices/ \;
rm -rf ./label_source/; mkdir ./label_source/; find ./C/ -type f -name '*.pkl' -exec cp {} label_source/ \;
rm -rf ./slice_label/; mkdir ./slice_label/
time python data_preprocess.py
