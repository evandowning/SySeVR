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
  * Install [anaconda](https://docs.anaconda.com/anaconda/install/linux/) and create environments
    * `$ conda create -n vdl_data python=2.7`
    * `$ conda create -n vdl python=3.6`
  * Download [Apache Ant 1.9](https://ant.apache.org/bindownload.cgi)
  * Download [Java 7](https://www.oracle.com/java/technologies/javase/javase7-archive-downloads.html)
  * Modify `setup.sh` to point where `JAVA_HOME` and `Apache Ant` folders are located.
  * Install [joern 0.3.1](https://joern.readthedocs.io/en/latest/installation.html) via the following:
    ```

    $ mkdir /data/joern/
    $ cp setup.sh /data/joern/
    $ cd /data/joern/

    $ conda activate vdl_data
    (vdl_data) $ ./setup.sh
    (vdl_data) $ conda install -c conda-forge python-igraph
    ```
  * Run [experiments](experiments.md)
