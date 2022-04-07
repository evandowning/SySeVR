#!/bin/bash

rm -rf ./data/; mkdir -p ./data/data_source/SARD/; mkdir -p ./data/label_source/SARD/; mkdir -p ./data/corpus/SARD/

cp ../source2slice/slice_label/* ./data/data_source/SARD/
cp ../source2slice/label_source/* ./data/label_source/SARD/

# Takes about 23 seconds for CWE416
time python process_dataflow_func.py

# Takes about 5 minutes for CWE416
rm -rf ./w2v_model; mkdir ./w2v_model/
time python create_w2vmodel.py

# Takes 10 seconds for CWE416
mkdir -p ./data/vector/SARD/; rm -rf ./dl_input/; mkdir -p ./dl_input/cdg_ddg/train/; mkdir -p ./dl_input/cdg_ddg/test/
time python get_dl_input.py

# Takes 1 second for CWE416
rm -rf ./dl_input_shuffle/; mkdir -p ./dl_input_shuffle/cdg_ddg/train/; mkdir -p ./dl_input_shuffle/cdg_ddg/test/
time python dealrawdata.py
