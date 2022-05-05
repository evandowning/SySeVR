#!/bin/bash

for id in 121 122 190 191 415 416; do
    time /data/evan/joern/jdk1.7.0_80/bin/java -jar /data/evan/joern/joern-0.3.1/bin/joern.jar "/data/evan/vulchecker/labeled-dataset-master/CWE${id}/source_files/" > "joern_${id}_stdout.txt" 2> "joern_${id}_stderr.txt"
done
