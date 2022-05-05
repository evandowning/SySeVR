# Parse Dataset
  * Load data via Joern
    ```
    # The following will create ".joernIndex/"

    $ cd Implementation/source2slice/

    # Takes about 11 minutes
    $ time ./import.sh
    ```
  * Start Neo4j console
    ```
    # Modify Neo4j config files as needed: https://joern.readthedocs.io/en/latest/import.html
    # I.e., point it to the .joernIndex folder

    $ cd /data/joern/neo4j-community-2.1.8/
    $ ulimit -n 60000
    $ vim ./conf/neo4j-wrapper.conf
        Add "wrapper.java.maxmemory=29000"
        Add "wrapper.java.additional=-XX:PermSize=256m"
        Add "wrapper.java.additional=-XX:MaxPermSize=512m"
    $ JAVA_HOME=/data/evan/joern/jdk1.7.0_80/ ./bin/neo4j console
    ```
  * Parse dataset
    ```
    $ cd Implementation/source2slice/

    $ conda activate vdl_data

    # Takes about 10 seconds
    (vdl_data) $ ./create_label.sh

    # Bad practice, but I just copy the "Implementation/" folder for each of the CWEs -- makes things easier to run for now.
    # Just make sure you restart Neo4j each time so it's accessing the correct .joernIndex folder location

    # Takes about 50 minutes
    (vdl_data) $ ./set_416.sh
    (vdl_data) $ time ./extract.sh &> extract_416_stdout_stderr.txt
    ```
  * Exit Neo4j console (you won't need it anymore)

# Preprocess Dataset
  * Create an Anaconda environment `vdl` that uses Python 3.6
  * Preprocess dataset
    ```
    $ cd Implementation/data_preprocess/

    $ conda activate vdl
    (vdl) $ conda install -c glemaitre imbalanced-learn
    (vdl) $ pip install -r requirements.txt

    # Takes about 1 minute
    (vdl) $ time ./preprocess.sh
    ```

# Train Models
```
$ cd Implementation/model/

$ conda activate vdl

(vdl) $ ./clean.sh

# Takes about 35 minutes
(vdl) $ time python bgru.py &> bgru_stdout_stderr.txt
```
