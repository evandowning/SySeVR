# Parse Dataset
  * Load data via Joern
    ```
    # The following will create ".joernIndex/"

    $ cd Implementation/source2slice/

    # Takes about 25 minutes
    $ time ./import.sh
    ```
  * Start Neo4j console
    ```
    # Modify Neo4j config files as needed: https://joern.readthedocs.io/en/latest/import.html

    $ cd /data/joern/neo4j-community-2.1.8/
    $ ulimit -n 60000
    $ vim ./conf/neo4j-wrapper.conf
        Add "wrapper.java.maxmemory=29000"
        Add "wrapper.java.additional=-XX:PermSize=256m"
        Add "wrapper.java.additional=-XX:MaxPermSize=512m"
    $ JAVA_HOME=/data/evan/joern/jdk1.7.0_80/ ./bin/neo4j console
    ```
  * Install Anaconda and create an environment `vdl_data` that uses Python 2.7.18
  * Parse dataset
    ```
    $ cd Implementation/source2slice/

    # Takes about 14 minutes
    $ ./create_label.sh

    $ conda activate vdl_data

    # Takes about 3300 minutes (2.3 days)
    (vdl_data) $ time ./extract.sh &> extract_stdout_stderr.txt
    ```
  * Exit Neo4j console

# Preprocess Dataset
  * Create an Anaconda environment `vdl` that uses Python 3.6
  * Preprocess dataset
    ```
    $ cd Implementation/data_preprocess/

    $ conda activate vdl
    $ conda install -c glemaitre imbalanced-learn

    # Takes about 
    (vdl) $ time ./preprocess.sh
    ```

# Train Models
```
$ cd Implementation/model/

$ rm -rf ./model/; mkdir ./model/
$ rm -rf ./result/; mkdir -p ./result/BGRU/
$ rm -rf ./result_analyze/; mkdir -p ./result_analyze/BGRU/

$ conda activate vdl

# Takes about 
(vdl) $ time python bgru.py
```
