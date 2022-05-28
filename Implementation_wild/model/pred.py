import sys
import os
from bgru import build_model
from preprocess_dl_Input_version5 import *

from sklearn import metrics

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def _main(datasetpath, weightpath, batch_size, maxlen, vector_dim, layers, dropout, outFN, labelMap):
    # Construct model
    model = build_model(maxlen, vector_dim, layers, dropout)

    # Load weights of trained model
    model.load_weights(weightpath)

    with open(outFN,'w') as fw:
        for filename in os.listdir(datasetpath):
            sys.stderr.write('Parsing {0}\n'.format(filename))
            f = open(datasetpath+filename, "rb")
            data = pickle.load(f,encoding="latin1")
            f.close()

            d = process_sequences_shape(data[0],maxlen,vector_dim)

            labels = model.predict(x = d,batch_size = 1)
            for i in range(len(labels)):
                srcLine = data[3][i]
                prediction = labels[i][0]
                true_label = data[1][i]

                srcFile    = srcLine.split(' ')[1]
                srcLineNum = srcLine.split(' ')[-1]

                # Get label for this line (true_label doesn't have anything in it)
                base = '/'.join(srcFile.split('/')[5:])
                baseFolder = base.split('/')[0]
                rest = '/'.join(base.split('/')[1:])
                base = os.path.join('/mnt/sdb/gmacon3/labeled-dataset/samples-from-wild/', baseFolder, 'hector_build/../', rest)

                if base not in labelMap:
                    true_label = 0
                else:
                    if srcLineNum in labelMap[base]:
                        true_label = 1

                        # Remove line from label map
                        labelMap[base].remove(srcLineNum)
                    else:
                        true_label = 0

                # Source line, prediction, label
                fw.write('{0}\t{1}\t{2}\t{3}\n'.format(srcFile,srcLineNum,prediction,true_label))

        # Output remaining (missing) labels
       #for k,v in labelMap.items():
       #    # Ignore linux
       #    if 'x86_64-linux-gnu' in k:
       #        continue

       #    for n in v:
       #        fw.write('{0}\t{1}\t0\t1\n'.format(k,n))

def get_label(labelFN):
    labels = dict()

    with open(labelFN,'r') as fr:
        for e,line in enumerate(fr):
            if e == 0:
                continue

            line = line.strip('\n')

            src,num = line.split('\t')
            if src not in labels.keys():
                labels[src] = set()
            labels[src].add(num)

    return labels

if __name__ == '__main__':
    weightPath = sys.argv[1]
    labelFN = sys.argv[2]
    trainFN = sys.argv[3]
    testFN = sys.argv[4]

    # Read in label file
    labels = get_label(labelFN)

    batchSize = 32
    vectorDim = 40
    maxLen = 500
    layers = 2
    dropout = 0.2
    traindataSetPath = "../data_preprocess/dl_input_shuffle/cdg_ddg/train/"
    testdataSetPath = "../data_preprocess/dl_input_shuffle/cdg_ddg/test/"
    _main(traindataSetPath, weightPath, batchSize, maxLen, vectorDim, layers, dropout, trainFN, labels)
    _main(testdataSetPath,  weightPath, batchSize, maxLen, vectorDim, layers, dropout, testFN, labels)
