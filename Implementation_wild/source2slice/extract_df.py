## coding:utf-8
from joern.all import JoernSteps
from igraph import *
from access_db_operate import *
from slice_op import *
from py2neo.packages.httpstream import http
http.socket_timeout = 9999

from parsed_label_files import *

def get_slice_file_sequence(store_filepath, list_result, count, func_name, startline, filepath_all):
    list_for_line = []
    statement_line = 0
    vulnline_row = 0
    list_write2file = []

    for node in list_result:    
        if node['type'] == 'Function':
            f2 = open(node['filepath'], 'r')
            content = f2.readlines()
            f2.close()
            raw = int(node['location'].split(':')[0])-1
            code = content[raw].strip()

            new_code = ""
            if code.find("#define") != -1:
                list_write2file.append(code + ' ' + str(raw+1) + '\n')
                continue

            while (len(code) >= 1 and code[-1] != ')' and code[-1] != '{'):
                if code.find('{') != -1:
                    index = code.index('{')
                    new_code += code[:index].strip()
                    list_write2file.append(new_code + ' ' + str(raw+1) + '\n')
                    break

                else:
                    new_code += code + '\n'
                    raw += 1
                    code = content[raw].strip()
                    #print "raw", raw, code

            else:
                new_code += code
                new_code = new_code.strip()
                if new_code[-1] == '{':
                    new_code = new_code[:-1].strip()
                    list_write2file.append(new_code + ' ' + str(raw+1) + '\n')
                    #list_line.append(str(raw+1))
                else:
                    list_write2file.append(new_code + ' ' + str(raw+1) + '\n')
                    #list_line.append(str(raw+1))

        elif node['type'] == 'Condition':
            raw = int(node['location'].split(':')[0])-1
            if raw in list_for_line:
                continue
            else:
                #print node['type'], node['code'], node['name']
                f2 = open(node['filepath'], 'r')
                content = f2.readlines()
                f2.close()
                code = content[raw].strip()
                pattern = re.compile("(?:if|while|for|switch)")
                #print code
                res = re.search(pattern, code)
                if res == None:
                    raw = raw - 1
                    code = content[raw].strip()
                    new_code = ""

                    while (code[-1] != ')' and code[-1] != '{'):
                        if code.find('{') != -1:
                            index = code.index('{')
                            new_code += code[:index].strip()
                            list_write2file.append(new_code + ' ' + str(raw+1) + '\n')
                            #list_line.append(str(raw+1))
                            list_for_line.append(raw)
                            break

                        else:
                            new_code += code + '\n'
                            list_for_line.append(raw)
                            raw += 1
                            code = content[raw].strip()

                    else:
                        new_code += code
                        new_code = new_code.strip()
                        if new_code[-1] == '{':
                            new_code = new_code[:-1].strip()
                            list_write2file.append(new_code + ' ' + str(raw+1) + '\n')
                            #list_line.append(str(raw+1))
                            list_for_line.append(raw)

                        else:
                            list_for_line.append(raw)
                            list_write2file.append(new_code + ' ' + str(raw+1) + '\n')
                            #list_line.append(str(raw+1))

                else:
                    res = res.group()
                    if res == '':
                        print filepath_all + ' ' + func_name + " error!"
                        exit()

                    elif res != 'for':
                        new_code = res + ' ( ' + node['code'] + ' ) '
                        list_write2file.append(new_code + ' ' + str(raw+1) + '\n')
                        #list_line.append(str(raw+1))

                    else:
                        new_code = ""
                        if code.find(' for ') != -1:
                            code = 'for ' + code.split(' for ')[1]

                        while code != '' and code[-1] != ')' and code[-1] != '{':
                            if code.find('{') != -1:
                                index = code.index('{')
                                new_code += code[:index].strip()
                                list_write2file.append(new_code + ' ' + str(raw+1) + '\n')
                                #list_line.append(str(raw+1))
                                list_for_line.append(raw)
                                break

                            elif code[-1] == ';' and code[:-1].count(';') >= 2:
                                new_code += code
                                list_write2file.append(new_code + ' ' + str(raw+1) + '\n')
                                #list_line.append(str(raw+1))
                                list_for_line.append(raw)
                                break

                            else:
                                new_code += code + '\n'
                                list_for_line.append(raw)
                                raw += 1
                                code = content[raw].strip()

                        else:
                            new_code += code
                            new_code = new_code.strip()
                            if new_code[-1] == '{':
                                new_code = new_code[:-1].strip()
                                list_write2file.append(new_code + ' ' + str(raw+1) + '\n')
                                #list_line.append(str(raw+1))
                                list_for_line.append(raw)

                            else:
                                list_for_line.append(raw)
                                list_write2file.append(new_code + ' ' + str(raw+1) + '\n')
                                #list_line.append(str(raw+1))
        
        elif node['type'] == 'Label':
            f2 = open(node['filepath'], 'r')
            content = f2.readlines()
            f2.close()
            raw = int(node['location'].split(':')[0])-1
            code = content[raw].strip()
            list_write2file.append(code + ' ' + str(raw+1) + '\n')
            #list_line.append(str(raw+1))

        elif node['type'] == 'ForInit':
            continue

        elif node['type'] == 'Parameter':
            if list_result[0]['type'] != 'Function':
                row = node['location'].split(':')[0]
                list_write2file.append(node['code'] + ' ' + str(row) + '\n')
                #list_line.append(row)
            else:
                continue

        elif node['type'] == 'IdentifierDeclStatement':
            if node['code'].strip().split(' ')[0] == "undef":
                f2 = open(node['filepath'], 'r')
                content = f2.readlines()
                f2.close()
                raw = int(node['location'].split(':')[0])-1
                code1 = content[raw].strip()
                list_code2 = node['code'].strip().split(' ')
                i = 0
                while i < len(list_code2):
                    if code1.find(list_code2[i]) != -1:
                        del list_code2[i]
                    else:
                        break
                code2 = ' '.join(list_code2)

                list_write2file.append(code1 + ' ' + str(raw+1) + '\n' + code2 + ' ' + str(raw+2) + '\n')

            else:
                list_write2file.append(node['code'] + ' ' + node['location'].split(':')[0] + '\n')

        elif node['type'] == 'ExpressionStatement':
            row = int(node['location'].split(':')[0])-1
            if row in list_for_line:
                continue

            if node['code'] in ['\n', '\t', ' ', '']:
                list_write2file.append(node['code'] + ' ' + str(row+1) + '\n')
                #list_line.append(row+1)
            elif node['code'].strip()[-1] != ';':
                list_write2file.append(node['code'] + '; ' + str(row+1) + '\n')
                #list_line.append(row+1)
            else:
                list_write2file.append(node['code'] + ' ' + str(row+1) + '\n')
                #list_line.append(row+1)

        elif node['type'] == "Statement":
            row = node['location'].split(':')[0]
            list_write2file.append(node['code'] + ' ' + str(row) + '\n')
            #list_line.append(row+1)

        else:         
            #print node['name'], node['code'], node['type'], node['filepath']
            if node['location'] == None:
                continue
            f2 = open(node['filepath'], 'r')
            content = f2.readlines()
            f2.close()
            row = int(node['location'].split(':')[0])-1
            code = content[row].strip()
            if row in list_for_line:
                continue

            else:
                list_write2file.append(node['code'] + ' ' + str(row+1) + '\n')
                #list_line.append(str(row+1))

    f = open(store_filepath, 'a')
    f.write(str(count) + ' ' + filepath_all + ' ' + func_name + ' ' + startline + '\n')
    for wb in list_write2file:
        f.write(wb)
    f.write('------------------------------' + '\n')     
    f.close()



def program_slice(pdg, startnodesID, slicetype, testID):#process startnodes as a list, because main func has many different arguments
    list_startnodes = []
    if pdg == False or pdg == None:
        return [], [], []
        
    for node in pdg.vs:
        #print node['functionId']
        if node['name'] in startnodesID:
            list_startnodes.append(node)

    if list_startnodes == []:
        return [], [], []

    if slicetype == 0:#backwords
        start_line = list_startnodes[0]['location'].split(':')[0]
        start_name = list_startnodes[0]['name']
        startline_path = list_startnodes[0]['filepath']
        results_back = program_slice_backwards(pdg, list_startnodes)

        not_scan_func_list = []
        results_back, temp = process_cross_func(results_back, testID, 1, results_back, not_scan_func_list)


        return [results_back], start_line, startline_path

    elif slicetype == 1:#forwords
#       print "start extract forword dataflow!"
#       print list_startnodes, startnodesID
        start_line = list_startnodes[0]['location'].split(':')[0]
        start_name = list_startnodes[0]['name']
        startline_path = list_startnodes[0]['filepath']
        results_for = program_slice_forward(pdg, list_startnodes)

        not_scan_func_list = []
        results_for, temp = process_cross_func(results_for, testID, 1, results_for, not_scan_func_list)

        return [results_for], start_line, startline_path

    else:#bi_direction
#       print "start extract backwords dataflow!"

        start_line = list_startnodes[0]['location'].split(':')[0]
        start_name = list_startnodes[0]['name']
        startline_path = list_startnodes[0]['filepath']
        results_back = program_slice_backwards(pdg, list_startnodes)#results_back is a list of nodes

        results_for = program_slice_forward(pdg, list_startnodes)      
        

        _list_name = []
        for node_back in results_back:
            _list_name.append(node_back['name'])

        for node_for in results_for:
            if node_for['name'] in _list_name:
                continue
            else:
                results_back.append(node_for)

        results_back = sortedNodesByLoc(results_back)
       
        iter_times = 0
        start_list = [[results_back, iter_times]]
        i = 0
        not_scan_func_list = []
        list_cross_func_back, not_scan_func_list = process_crossfuncs_back_byfirstnode(start_list, testID, i, not_scan_func_list)
        list_results_back = [l[0] for l in list_cross_func_back]
      
        all_result = [] 
        for results_back in list_results_back:
            index = 1
            for a_node in results_back:
                if a_node['name'] == start_name:
                    break
                else:
                    index += 1

            list_to_crossfunc_back = results_back[:index]
            list_to_crossfunc_for = results_back[index:]

            list_to_crossfunc_back, temp = process_cross_func(list_to_crossfunc_back, testID, 0, list_to_crossfunc_back, not_scan_func_list)

            list_to_crossfunc_for, temp = process_cross_func(list_to_crossfunc_for, testID, 1, list_to_crossfunc_for, not_scan_func_list)

            all_result.append(list_to_crossfunc_back + list_to_crossfunc_for)
  

        return all_result, start_line, startline_path


def api_slice():
    count = 1
    store_filepath = "C/test_data/4/api_slices.txt"
    f = open("sensifunc_slice_points.pkl", 'rb')

    while True:
        try:
            dict_unsliced_sensifunc = pickle.load(f)
        except EOFError:
            break

        total = len(dict_unsliced_sensifunc.keys())

        func_count = 0

        for e,key in enumerate(dict_unsliced_sensifunc.keys()):#key is testID
            func_count += len(dict_unsliced_sensifunc[key])

            #sys.stderr.write('Processing {0}/{1}\r'.format(e+1,total))
            sys.stderr.write('Processing {0}/{1}/{2}\r'.format(e+1,total,func_count))
            sys.stderr.flush()

           #print('key: ',key)

            for _t in dict_unsliced_sensifunc[key]:
                list_sensitive_funcid = _t[0]
                pdg_funcid = _t[1]
                sensitive_funcname = _t[2]

                if sensitive_funcname.find("main") != -1:
                    continue
                else:
                    slice_dir = 2

                    pdg = getFuncPDGById(key, pdg_funcid)
                    if pdg == False:
                        print 'error'
                        exit()

                    f_path = pdg.vs[0]['filepath']
                    if f_path not in files_of_interest:
                        continue

                    list_code, startline, startline_path = program_slice(pdg, list_sensitive_funcid, slice_dir, key)
                    #print len(list_code)

                    if list_code == []:
                        fout = open("error.txt", 'a')
                        fout.write(sensitive_funcname + ' ' + str(list_sensitive_funcid) + ' found nothing! \n')
                        fout.close()
                    else:
                        for _list in list_code:
                            try:
                                get_slice_file_sequence(store_filepath, _list, count, sensitive_funcname, startline, startline_path)
                            except:
                                pass
                            count += 1

        if len(dict_unsliced_sensifunc.keys()) > 0:
            sys.stderr.write('\n')

    f.close()

def pointers_slice():
    count = 1
    store_filepath = "C_pointer/test_data/4/pointersuse_slices.txt"
    f = open("pointuse_slice_points.pkl", 'rb')
    dict_unsliced_pointers = pickle.load(f)
#   print dict_unsliced_pointers
    f.close()

    total = len(dict_unsliced_pointers.keys())

    func_count = 0

    l = []
    for e,key in enumerate(dict_unsliced_pointers.keys()):#key is testID
        func_count += len(dict_unsliced_pointers[key])
        #sys.stderr.write('Processing {0}/{1}\r'.format(e+1,total))
        sys.stderr.write('Processing {0}/{1}/{2}\r'.format(e+1,total,func_count))
        sys.stderr.flush()

        if key in l:
            continue

        for _t in dict_unsliced_pointers[key]:
            list_pointers_funcid = _t[0]
            pdg_funcid = _t[1]
            #print '\t',key, pdg_funcid
            pointers_name = str(_t[2])

            slice_dir = 2
            pdg = getFuncPDGById(key, pdg_funcid)
            if pdg == False:
                print 'error'
                exit()

            f_path = pdg.vs[0]['filepath']
            if f_path not in files_of_interest:
                continue

            list_code, startline, startline_path = program_slice(pdg, list_pointers_funcid, slice_dir, key)

            if list_code == []:
                fout = open("error.txt", 'a')
                fout.write(pointers_name + ' ' + str(list_pointers_funcid) + ' found nothing! \n')
                fout.close()
            else:
                for _list in list_code:
                    try:
                        get_slice_file_sequence(store_filepath, _list, count, pointers_name, startline, startline_path)
                    except:
                        pass
                    count += 1

    sys.stderr.write('\n')

def arrays_slice():
    count = 1
    store_filepath = "C_arrays/test_data/4/arraysuse_slices.txt"
    f = open("arraysuse_slice_points.pkl", 'rb')
    dict_unsliced_pointers = pickle.load(f)
    f.close()

    total = len(dict_unsliced_pointers.keys())

    func_count = 0

    l = []
    for e,key in enumerate(dict_unsliced_pointers.keys()):#key is testID
        func_count += len(dict_unsliced_pointers[key])
        #sys.stderr.write('Processing {0}/{1}\r'.format(e+1,total))
        sys.stderr.write('Processing {0}/{1}/{2}\r'.format(e+1,total,func_count))
        sys.stderr.flush()

        #print(key)
        if key in l:
            continue

        for _t in dict_unsliced_pointers[key]:
            list_pointers_funcid = _t[0]
            pdg_funcid = _t[1]
#           print pdg_funcid
            arrays_name = str(_t[2])


            slice_dir = 2
            pdg = getFuncPDGById(key, pdg_funcid)
            if pdg == False:
                print 'error'
                exit()


            f_path = pdg.vs[0]['filepath']
            if f_path not in files_of_interest:
                continue

            list_code, startline, startline_path = program_slice(pdg, list_pointers_funcid, slice_dir, key)

            if list_code == []:
                fout = open("error.txt", 'a')
                fout.write(arrays_name + ' ' + str(list_pointers_funcid) + ' found nothing! \n')
                fout.close()
            else:
                for _list in list_code:
                    try:
                        get_slice_file_sequence(store_filepath, _list, count, arrays_name, startline, startline_path)
                    except:
                        pass
                    count += 1
    sys.stderr.write('\n')


def integeroverflow_slice():
    count = 1
    store_filepath = "C_integer/test_data/4/integeroverflow_slices.txt"
    f = open("integeroverflow_slice_points_new.pkl", 'rb')
    dict_unsliced_expr = pickle.load(f)
    f.close()

    total = len(dict_unsliced_expr.keys())

    func_count = 0

    l = []
    for e,key in enumerate(dict_unsliced_expr.keys()):#key is testID
        func_count += len(dict_unsliced_expr[key])
        #sys.stderr.write('Processing {0}/{1}\r'.format(e+1,total))
        sys.stderr.write('Processing {0}/{1}/{2}\r'.format(e+1,total,func_count))
        sys.stderr.flush()

        #print(key)

        if key in l:
            continue
        for _t in dict_unsliced_expr[key]:
            list_expr_funcid = _t[0]
            pdg_funcid = _t[1]
#           print pdg_funcid
            expr_name = str(_t[2])


            slice_dir = 2
            pdg = getFuncPDGById(key, pdg_funcid)
            if pdg == False:
                print 'error'
                exit()

            f_path = pdg.vs[0]['filepath']
            if f_path not in files_of_interest:
                continue

            list_code, startline, startline_path = program_slice(pdg, list_expr_funcid, slice_dir, key)

            if list_code == []:
                fout = open("error.txt", 'a')
                fout.write(expr_name + ' ' + str(list_expr_funcid) + ' found nothing! \n')
                fout.close()
            else:
                for _list in list_code:
                    try:
                        get_slice_file_sequence(store_filepath, _list, count, expr_name, startline, startline_path)
                    except:
                        pass
                    count += 1
    sys.stderr.write('\n')
     

if __name__ == "__main__":
    print 'api slice'
    api_slice()
    print 'pointers slice'
    pointers_slice()
    print 'arrays slice'
    arrays_slice()
    print 'integeroverflow slice'
    integeroverflow_slice()
