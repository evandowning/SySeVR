## coding:utf-8
import os
import pickle


f = open("dict_cwe2father.pkl", 'rb')
dict_cwe2father = pickle.load(f)
f.close()

#print dict_cwe2father['CWE-787']

#f = open("label_vec_type.pkl", 'rb')
f = open("label_vec_type_new.pkl", 'rb')
label_vec_type = pickle.load(f)
f.close()

#f = open("dict_testcase2code.pkl",'rb')
f = open("dict_testcase2code_new.pkl",'rb')
dict_testcase2code = pickle.load(f)
f.close()


def get_label_veclist(list_cwe):
    list_label = [0] * len(label_vec_type)
    for cweid in list_cwe:
        index = label_vec_type.index(cweid)
        list_label[index] = 1

    return list_label


def get_label_cwe(cweid, label_cwe):
    if cweid in label_vec_type:
        label_cwe.append(cweid)
        return label_cwe

    else:
        if cweid == 'CWE-1000':
            label_cwe = label_vec_type
        else:
            fathercweid = dict_cwe2father[cweid]

            for _id in fathercweid:
                label_cwe = get_label_cwe(_id, label_cwe)

    return label_cwe


# NOTE: because create_label.py extracted source line may not (exactly) match what
#       was parsed: "free(data);" versus "free ( data );"
def make_label(path, dict_vuln2testcase, _type):
    f = open(path, 'r')
    context = f.read().split('------------------------------')[:-1]
    f.close()

    context[0] = '\n' + context[0]

    list_all_label = list()
    list_all_vulline = list()

    for _slice in context:
        list_label = [0] * len(label_vec_type)
        vulline = list()

        index_line = _slice.split('\n')[1]

        # NOTE: fixes parsing error
        if ' ' not in index_line:
            continue

        list_codes = _slice.split('\n')[2:-1]
        key_name = index_line.split(' ')[1]

        # If we have a label for this source file
        if key_name in dict_vuln2testcase.keys():
            # Get CWE labels for lines
            labels_true = dict_vuln2testcase[key_name]

            # Get CWE
            cwe = labels_true[0].values()[0]

            # Create list label
            list_label = get_label_veclist([cwe])

            # Get each line number in source file
            line_numbers = [code.split(' ')[-1] for code in list_codes]

            # For each vulnerable line, get line index in codelist
            vulline = [line_numbers.index(d.keys()[0]) for d in labels_true if d.keys()[0] in line_numbers]

            # If vulnerable line didn't exist, clear list_label
            if len(vulline) == 0:
                list_label = [0] * len(label_vec_type)

        # Append data to lists
        list_all_label.append(list_label)
        list_all_vulline.append(vulline)

    return list_all_label, list_all_vulline

def main():
    #f = open("dict_flawline2filepath.pkl", 'rb')
    f = open("dict_flawline2filepath_new.pkl", 'rb')
    dict_vuln2testcase = pickle.load(f)
    f.close()
    _type = False
    time = '4'
    lang = 'C/test_data/' + time
    
    path = os.path.join(lang, 'api_slices.txt')
    if os.path.exists(path):
        list_all_apilabel, list_all_vulline = make_label(path, dict_vuln2testcase, _type)
        dec_path = os.path.join(lang, 'api_slices_label.pkl')
        f = open(dec_path, 'wb')
        pickle.dump(list_all_apilabel, f, True)
        f.close()
        dec_path = os.path.join(lang, 'api_slices_vulline.pkl')
        f = open(dec_path, 'wb')
        pickle.dump(list_all_vulline, f)
        f.close()
    
    path = os.path.join(lang, 'arraysuse_slices.txt')
    if os.path.exists(path):
        list_all_arraylabel,_ = make_label(path, dict_vuln2testcase, _type)
        dec_path = os.path.join(lang, 'arraysuse_slices_label.pkl')
        f = open(dec_path, 'wb')
        pickle.dump(list_all_arraylabel, f, True)
        f.close()
    
    path = os.path.join(lang, 'pointersuse_slices.txt')
    if os.path.exists(path):
        list_all_pointerlabel,_ = make_label(path, dict_vuln2testcase, _type)
        dec_path = os.path.join(lang, 'pointersuse_slices_label.pkl')
        f = open(dec_path, 'wb')
        pickle.dump(list_all_pointerlabel, f, True)
        f.close()
 
    path = os.path.join(lang, 'integeroverflow_slices.txt')
    if os.path.exists(path):
        list_all_exprlabel,_ = make_label(path, dict_vuln2testcase, _type)
        dec_path = os.path.join(lang, 'integeroverflow_slices_label.pkl')
        f = open(dec_path, 'wb')
        pickle.dump(list_all_exprlabel, f, True)
        f.close()
    

if __name__ == '__main__':
    main()
