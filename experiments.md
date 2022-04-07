# Parse Dataset
  * Load data via Joern
    ```
    # The following will create ".joernIndex/"

    $ cd Implementation/source2slice/

    # Takes about 45 seconds
    $ time /data/evan/joern/jdk1.7.0_80/bin/java -jar /data/evan/joern/joern-0.3.1/bin/joern.jar /data/evan/vulchecker/labeled-dataset-master/CWE416/source_files/ > joern_416_stdout.txt 2> joern_416_stderr.txt
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
    (vdl_data) $ time ./extract.sh
    ```
  * Exit Neo4j console

# Preprocess Dataset
  * Create an Anaconda environment `vdl` that uses Python 3.6
  * Preprocess dataset
    ```
    $ cd Implementation/data_preprocess/

    $ conda activate vdl
    $ conda install -c glemaitre imbalanced-learn
    (vdl) $ time ./preprocess.sh
    ```

# Train Models
```
$ cd Implementation/model/

$ rm -rf ./model/; mkdir ./model/
$ rm -rf ./result/; mkdir -p ./result/BGRU/
$ rm -rf ./result_analyze/; mkdir -p ./result_analyze/BGRU/

$ conda activate vdl
(vdl) $ time python bgru.py
```
