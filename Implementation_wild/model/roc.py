import sys
import os
from bgru import build_model
from preprocess_dl_Input_version5 import *

from sklearn import metrics

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def _main(datasetpath, weightpath, batch_size, maxlen, vector_dim, layers, dropout, outFN, graphFN):
    # Construct model
    model = build_model(maxlen, vector_dim, layers, dropout)

    # Load weights of trained model
    model.load_weights(weightpath)

    roc_y = list()
    roc_score = list()

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

                # Source line, prediction, label
                fw.write('{0}\t{1}\t{2}\n'.format(srcLine,prediction,true_label))

                roc_y.append(float(true_label))
                roc_score.append(float(prediction))

    # Create ROC data
    fpr, tpr, thresholds = metrics.roc_curve(roc_y, roc_score)
    roc_auc = metrics.auc(fpr, tpr)

    # Graph ROC curve
    plt.plot(fpr,tpr,'r--')
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.title('Function ROC Curve. AUC = {0}'.format(round(roc_auc,4)))

    plt.savefig(graphFN)
    plt.clf()

if __name__ == '__main__':
    weightPath = sys.argv[1]
    trainFN = sys.argv[2]
    testFN = sys.argv[3]

    batchSize = 32
    vectorDim = 40
    maxLen = 500
    layers = 2
    dropout = 0.2
    traindataSetPath = "../data_preprocess/dl_input_shuffle/cdg_ddg/train/"
    testdataSetPath = "../data_preprocess/dl_input_shuffle/cdg_ddg/test/"
#   weightPath = './model/BRGU'
#   _main(traindataSetPath, weightPath, batchSize, maxLen, vectorDim, layers, dropout, 'roc_train.tsv', 'roc_train.png')
#   _main(testdataSetPath,  weightPath, batchSize, maxLen, vectorDim, layers, dropout, 'roc_test.tsv', 'roc_test.png')
    _main(traindataSetPath, weightPath, batchSize, maxLen, vectorDim, layers, dropout, trainFN, 'roc_train.png')
    _main(testdataSetPath,  weightPath, batchSize, maxLen, vectorDim, layers, dropout, testFN, 'roc_test.png')
