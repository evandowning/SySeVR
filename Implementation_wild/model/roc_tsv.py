import sys
import os

from sklearn import metrics

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def _main(predFN,graphFN):
    roc_y = list()
    roc_score = list()

    with open(predFN,'r') as fr:
        for line in fr:
            line = line.strip('\n')

            srcfile,srcline,pred,label = line.split('\t')

            roc_y.append(float(label))
            roc_score.append(float(pred))

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
    predFN = sys.argv[1]
    graphFN = sys.argv[2]

    _main(predFN,graphFN)
