#!/bin/bash

run() {
    software="${HOME}/software/"
    base="${HOME}/labeled-dataset-master/"
    id="$1"

    time "${software}/jdk1.7.0_80/bin/java" -jar "${software}/joern-0.3.1/bin/joern.jar" "${base}/${id}" > "joern_${id}_stdout.txt" 2> "joern_${id}_stderr.txt"

    mv "./.joernIndex/" "./.joernIndex_${id}/"
}

run "samples-from-wild_sourceonly"
