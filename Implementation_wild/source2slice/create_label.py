import sys
import os
import argparse
import json
import pickle

def _main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', help='dataset folder', required=True)
    parser.add_argument('--outcode', help='output code filename', required=True)
    parser.add_argument('--outpath', help='output path filename', required=True)
    parser.add_argument('--outvuln', help='output path filename', required=True)

    args = parser.parse_args()

    # Store arguments
    folder = args.folder
    codeFN = args.outcode
    pathFN = args.outpath
    vulnFN = args.outvuln

    codeDict = dict()
    pathDict = dict()
    vulnList = set()

    # For each CWE
    for cweFolder in os.listdir(folder):
        if 'CWE' not in cweFolder:
            continue

        labelFolder = os.path.join(folder,cweFolder,'source_labels','individual')

        # For each source file label
        for fn in os.listdir(labelFolder):
            path = os.path.join(labelFolder,fn)

            cweLabel = fn.split('_')[0]
            cweLabel = cweLabel.replace('CWE','CWE-')

            vulnList.add(cweLabel)

            # Read file content
            with open(path,'r') as fr:
                content = json.load(fr)

            # Read source file content
            sourceFN = fn.replace('.json','')
            sourcePath = os.path.join(folder,cweFolder,'source_files',sourceFN)
            with open(sourcePath,'r') as fr:
                sourceContent = fr.readlines()

            # For each vulnerable line
            for entry in content:
                entry_ln = entry['line_number']

                # Get source line
                source_line = sourceContent[entry_ln-1] # -1 because it's 0 indexed

                # Insert into code dictionary
                key = '{0}/{1}'.format(sourcePath,entry_ln)
                value = source_line
                codeDict[key] = value

                # Insert into path dictionary
                key = sourcePath
                if key not in pathDict.keys():
                    pathDict[key] = list()

                value = dict({str(entry_ln): cweLabel})
                pathDict[key].append(value)

#           print(path)
#           print(sourcePath)
#           print('')
#           print(codeDict)
#           print('')
#           print(pathDict)

    # Output files
    with open(codeFN,'wb') as fw:
        pickle.dump(codeDict, fw, True)
    with open(pathFN,'wb') as fw:
        pickle.dump(pathDict, fw, True)
    with open(vulnFN,'wb') as fw:
        pickle.dump(list(vulnList), fw, True)

if __name__ == '__main__':
    _main()
