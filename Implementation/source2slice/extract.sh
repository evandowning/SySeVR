#!/bin/bash

#   # Takes 12 minutes for CWE416
#   # Takes 523 minutes for everything
#   rm -rf ./cfg_db/; mkdir ./cfg_db/
#   time python get_cfg_relation.py

#   # Takes 45 minutes for CWE416
#   # Takes 1864 minutes for everything
#   rm -rf ./pdg_db/; mkdir ./pdg_db/
#   time python complete_PDG.py

#   # Takes 1 minute for CWE416
#   # Takes 766 minutes for everything
#   rm -rf ./dict_call2cfgNodeID_funcID/; mkdir ./dict_call2cfgNodeID_funcID/
#   time python access_db_operate.py

# Takes 16 minutes for CWE416
# Takes 2200 minutes for everything
# NOTE: will need to run this twice -- can't run all at once
#       Afterwards, can combine sensifunc_slice_points_part1.pkl and sensifunc_slice_points_part2.pkl
#       using combine.py
#   time python points_get.py

# Takes 5 minutes for CWE416
rm -rf ./C/; mkdir -p ./C/test_data/4/
rm -rf ./pdg_db/testCode/; mkdir -p ./pdg_db/testCode/
time python extract_df.py > extract_df_stdout.txt

exit

# Takes 17 seconds for CWE416
time python make_label.py

# Takes about 2 seconds for CWE416
rm -rf ./slices/; mkdir ./slices/; find ./C/ -type f -name '*.txt' -exec cp {} slices/ \;
rm -rf ./label_source/; mkdir ./label_source/; find ./C/ -type f -name '*.pkl' -exec cp {} label_source/ \;
rm -rf ./slice_label/; mkdir ./slice_label/
time python data_preprocess.py
