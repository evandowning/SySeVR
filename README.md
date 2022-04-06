SySeVR: A Framework for Using Deep Learning to Detect Vulnerabilities
=

We propose a general framework for using deep learning to detect vulnerabilities, named SySeVR. For evaluate the SySeVR, we collect the Semantics-based Vulnerability Candidate (SeVC) dataset, which contains all kinds of vulnerabilities that are available from the National Vulnerability Database (NVD) and the Software Assurance Reference Dataset (SARD).

At a high level, the SyVC representation corresponds to a piece of code in a program that may be vulnerable based on a syntax analysis. The SeVC representation corresponds to the extended statements of the SyVCs, with the extension to incorporate some of the other statements that are semantically related to the SyVCs.

SeVC dataset focuses on 1,591 open source C/C++ programs from the NVD and 14,000 programs from the SARD. It contains 420,627 SeVCs, including 56,395 vulnerable SeVCs and 364,232 SeVCs that are not vulnerable. Four types of SyVCs are involved.

1. Library/API Function Call : This accommodates the vulnerabilities that are related to library/API function calls.
2. Array Usage: This accommodates the vulnerabilities that are related to arrays (e.g., improper use in array element access, array address arithmetic, address transfer as a function parameter).
3. Pointer Usage: This accommodates the vulnerabilities that are related to pointers (e.g., improper use in pointer arithmetic, reference, address transfer as a function parameter).
4. Arithmetic Expression: This accommodates the vulnerabilities that are related to improper arithmetic expressions (e.g., integer overflow).

## Usage
  * Install anaconda and create an environment that uses Python 2.7
  * Download [Apache Ant 1.9](https://ant.apache.org/bindownload.cgi)
  * Download [Java 7](https://www.oracle.com/java/technologies/javase/javase7-archive-downloads.html)
  * Modify `setup.sh` to point where `JAVA_HOME` and `Apache Ant` folders are located.
  * Install [joern 0.3.1](https://joern.readthedocs.io/en/latest/installation.html)
    ```
    $ mkdir /data/joern/
    $ cp setup.sh /data/joern/
    $ cd /data/joern/

    $ ./setup.sh
    $ conda install -c conda-forge python-igraph
    ```
  * Extract data
    ```
    $ cd Implementation/source2slice/

    # Takes about minutes to run through SARD dataset
    # Takes about 50 minutes to run through entire dataset (NVD + SARD)
    # /data/evan/joern/jdk1.7.0_80/bin/java -jar /data/evan/joern/joern-0.3.1/bin/joern.jar /data/evan/SySeVR/Program\ data/SARD/SARD/


    # Takes about 15 minutes to run through entire dataset (NVD + SARD)
    $ mkdir ./mydata/
    $ cp /data/evan/SySeVR/Program\ data/SARD/SARD/ ./mydata/
    $ find mydata -type f -not -name '*.c*' -delete
    $ time /data/evan/joern/jdk1.7.0_80/bin/java -jar /data/evan/joern/joern-0.3.1/bin/joern.jar /data/evan/SySeVR/mydata/ > joern_stdout.txt 2> joern_stderr.txt
    # This will create a directory ".joernIndex/" in the current working directory
    # Make sure ".joernIndex/" doesn't exist before running this.

    # Modify Neo4j config files as needed: https://joern.readthedocs.io/en/latest/import.html

    $ cd /data/joern/neo4j-community-2.1.8/
    $ ulimit -n 60000
    $ vim conf/conf/neo4j-wrapper.conf
        Add "wrapper.java.maxmemory=29000"
        Add "wrapper.java.additional=-XX:PermSize=256m"
        Add "wrapper.java.additional=-XX:MaxPermSize=512m"
    $ JAVA_HOME=/data/evan/joern/jdk1.7.0_80/ ./bin/neo4j console

    $ cd Implementation/source2slice/

    # Takes about  1,730 minutes (1.2 days)
    $ mkdir cfg_db/
    $ python get_cfg_relation.py

    # Takes about 7,857 minutes (5.4 days)
    $ mkdir pdg_db/
    $ python complete_PDG.py

    # Takes about 608 minutes (10 hours)
    $ mkdir dict_call2cfgNodeID_funcID/
    $ python access_db_operate.py

    # Restart Neo4j in case it's using too much RAM.

    # Takes about 5 hours
    $ python points_get.py

    # Takes about 182 minutes
    $ rm -rf ./C/test_data/4; mkdir -p ./C/test_data/4/
    $ rm -rf ./pdg_db/testCode/; mkdir -p ./pdg_db/testCode/
    $ python extract_df.py

    # Takes about 
    $ python make_label.py

    $ rm -rf slices/; mkdir slices/; find ./C/ -type f -name '*.txt' -exec cp {} slices/ \;
    $ rm -rf label_source/; mkdir label_source/; find ./C/ -type f -name '*.pkl' -exec cp {} label_source/ \;
    $ rm -rf slice_label/; mkdir slice_label/

    # Takes about 
    $ python data_preprocess.py

    # Stop Neo4j (don't need it running anymore)
    ```
  * Install anaconda and create an environment that uses Python 3.6
    ```
    $ pip install -r /home/evan/repo/VulDeeLocator/requirements.txt
    ```
  * Preprocess data
    ```
    $ cd Implementation/data_preprocess/
    $ mkdir ./data/
    $ mkdir ./data/data_source/
    $ mkdir ./data/label_source/
    $ mkdir ./data/corpus/

    $ cp ../source2slice/slice_label/* ./data/data_source/SARD/
    $ cp ../source2slice/label_source/* ./data/label_source/SARD/
    $ mkdir ./data/corpus/SARD/

    $ python process_dataflow_func.py

    $ mkdir ./w2v_model/
    $ python create_w2vmodel.py

    $ mkdir -p ./data/vector/SARD/
    $ mkdir -p ./dl_input/cdg_ddg/train/
    $ mkdir -p ./dl_input/cdg_ddg/test/
    $ python get_dl_input.py

    $ mkdir -p ./dl_input_shuffle/cdg_ddg/train/
    $ mkdir -p ./dl_input_shuffle/cdg_ddg/test/
    $ conda install -c glemaitre imbalanced-learn
    $ python dealrawdata.py
    ```
  * Train data
    ```
    $ cd Implementation/model/

    # NOTE: VulDeeLocator has source code to keras the authors modified
    $ mkdir ./model/
    $ mkdir -p ./result/BGRU/
    $ mkdir -p ./result_analyze/BGRU/
    $ python bgru.py
    ```
