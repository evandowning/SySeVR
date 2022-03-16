#!/bin/bash

INSTALLDIR=`pwd`
JOERN=joern-0.3.1

#Dependancies
sudo apt-get -y install python-setuptools python-dev
sudo apt-get -y install graphviz libgraphviz-dev graphviz-dev
sudo apt-get -y install pkg-config
sudo apt-get -y install unzip

#Building joern
cd $INSTALLDIR
wget https://github.com/fabsx00/joern/archive/0.3.1.tar.gz
tar xfzv 0.3.1.tar.gz
cd joern-0.3.1
wget http://mlsec.org/joern/lib/lib.tar.gz
tar xfzv lib.tar.gz
JAVA_HOME=/data/evan/joern/jdk1.7.0_80/ /data/evan/joern/apache-ant-1.9.16/bin/ant
JAVA_HOME=/data/evan/joern/jdk1.7.0_80/ /data/evan/joern/apache-ant-1.9.16/bin/ant tools

#Neo4j 2.1.8
cd $INSTALLDIR
wget http://neo4j.com/artifact.php?name=neo4j-community-2.1.8-unix.tar.gz
tar -zxvf artifact.php\?name\=neo4j-community-2.1.8-unix.tar.gz
Neo4jDir="${INSTALLDIR}/neo4j-community-2.1.8/"
wget http://mlsec.org/joern/lib/neo4j-gremlin-plugin-2.1-SNAPSHOT-server-plugin.zip
unzip neo4j-gremlin-plugin-2.1-SNAPSHOT-server-plugin.zip -d "${Neo4jDir}/plugins/gremlin-plugin"

#py2neo 2.0
cd $INSTALLDIR
https://github.com/nigelsmall/py2neo/archive/refs/tags/py2neo-2.0.7.tar.gz
tar zxvf py2neo-2.0.7.tar.gz
cd py2neo-py2neo-2.0.7
python setup.py install

#Python-Joern
# TODO: uncomment py2neo requirement in setup.py
cd $INSTALLDIR
git clone https://github.com/fabsx00/python-joern.git
cd python-joern
python setup.py install

#Joern-Tools
cd $INSTALLDIR
git clone https://github.com/fabsx00/joern-tools.git
pip install pygraphviz
cd joern-tools
python setup.py install
