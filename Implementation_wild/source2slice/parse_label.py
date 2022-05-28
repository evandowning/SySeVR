import sys
import os

folder = '/home/evan/repo/SySeVR/Implementation_wild/model/wildcve_test/'

paths = set()

for root,dirs,files in os.walk(folder):
    for fn in files:
        path = os.path.join(root,fn)

        with open(path,'r') as fr:
            for line in fr:
                line = line.strip('\n')

                f,n = line.split('\t')

                if 'labeled-dataset' not in f:
                    continue

                interest_root='/home/evan/labeled-dataset-master/samples-from-wild_sourceonly/'

                base = '/'.join(f.split('/')[6:])
                baseFolder = base.split('/')[0]
                rest = '/'.join(base.split('/')[3:])

                final = os.path.join(interest_root,baseFolder,rest)

                paths.add(final)

# Output files to source file
with open('parsed_label_files.py','w') as fw:
    fw.write('files_of_interest = [')
    for p in paths:
        fw.write('"{0}"'.format(p))
        fw.write(',')
    fw.write(']')
