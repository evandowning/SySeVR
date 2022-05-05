## coding:utf-8
from access_db_operate import *


def get_all_sensitiveAPI(db,fout):
    fin = open("sensitive_func.pkl", 'rb')
    list_sensitive_funcname = pickle.load(fin)
    fin.close()

    length = len(list_sensitive_funcname)
    print 'len: ', length
#   list_sensitive_funcname = ['getwd']  # this worked just fine
    # Without anything, stops at 455
    list_sensitive_funcname = list_sensitive_funcname[455:] # this stops working at 'main'
    # After this line, script finishes

    _dict = {}
    for e,func_name in enumerate(list_sensitive_funcname):
        print 'getting calls for ', func_name, ' index: ', str(e)

        # TODO - make new dictionary each time & dump
        pickle.dump(_dict, fout, True)
        _dict = {}

        list_callee_cfgnodeID = []
        if func_name.find('main') != -1:
            list_main_func = []
            list_mainfunc_node = getFunctionNodeByName(db, func_name)

            if list_mainfunc_node != []:
                file_path = getFuncFile(db, list_mainfunc_node[0]._id)
                testID = file_path.split('/')[-1]
                testID = '_'.join(testID.split('_')[:-1])
                for mainfunc in list_mainfunc_node:
                    list_parameters = get_parameter_by_funcid(db, mainfunc._id)

                    if list_parameters != []:
                        list_callee_cfgnodeID.append([testID, ([str(v) for v in list_parameters], str(mainfunc._id), func_name)])

                    else:
                        continue

        else:
            list_callee_id = get_calls_id(db, func_name)
            if list_callee_id == []:
                continue

            for _id in list_callee_id:
                cfgnode = getCFGNodeByCallee(db, _id)
                if cfgnode != None:
                    file_path = getFuncFile(db, int(cfgnode.properties['functionId']))
                    testID = file_path.split('/')[-1]
                    testID = '_'.join(testID.split('_')[:-1])
                    list_callee_cfgnodeID.append([testID, ([str(cfgnode._id)], str(cfgnode.properties['functionId']), func_name)])

        if list_callee_cfgnodeID != []:
            for _l in list_callee_cfgnodeID:
                if _l[0] in _dict.keys():
                    _dict[_l[0]].append(_l[1])
                else:
                    _dict[_l[0]] = [_l[1]]

        else:
            continue

    return _dict


def get_all_pointer(db):
    _dict = {}
    list_pointers_node = get_pointers_node(db)
    for node_id in list_pointers_node:
        cfgnode = getNode(db, node_id)
        file_path = getFuncFile(db, int(cfgnode.properties['functionId']))
        testID = file_path.split('/')[-1]
        testID = '_'.join(testID.split('_')[:-1])
        pointer_defnode = get_def_node(db, cfgnode._id)
        pointer_name = []
        for node in pointer_defnode:
            name = node.properties['code'].replace('*', '').strip()
            if name not in pointer_name:
                pointer_name.append(name)

        if testID in _dict.keys():
            _dict[testID].append(([str(cfgnode._id)], str(cfgnode.properties['functionId']), pointer_name))
        else:
            _dict[testID] = [([str(cfgnode._id)], str(cfgnode.properties['functionId']), pointer_name)]

    return _dict


def get_all_array(db):
    _dict = {}
    list_arrays_node = get_arrays_node(db)
    for cfgnode in list_arrays_node:
        file_path = getFuncFile(db, int(cfgnode.properties['functionId']))
        testID = file_path.split('/')[-1]
        testID = '_'.join(testID.split('_')[:-1])
        array_defnode = get_def_node(db, cfgnode._id)
        array_name = []
        for node in array_defnode:
            name = node.properties['code'].replace('[', '').replace(']', '').replace('*', '').strip()
            if name not in array_name:
                array_name.append(name)

        if testID in _dict.keys():
            _dict[testID].append(([str(cfgnode._id)], str(cfgnode.properties['functionId']), array_name))
        else:
            _dict[testID] = [([str(cfgnode._id)], str(cfgnode.properties['functionId']), array_name)]

    return _dict


def get_all_pointer_use(db):
    _dict = {}
    list_pointers_node = get_pointers_node(db)
    for node_id in list_pointers_node:
        cfgnode = getNode(db, node_id)
        file_path = getFuncFile(db, int(cfgnode.properties['functionId']))
        testID = file_path.split('/')[-1]
        testID = '_'.join(testID.split('_')[:-1])
        pointer_defnode = get_def_node(db, cfgnode._id)

        _temp_list = []
        for node in pointer_defnode:
            name = node.properties['code'].strip()
            list_usenodes = get_all_use_bydefnode(db, node._id)
            list_defnodes = get_all_def_bydefnode(db, node._id)

            i = 0
            while i < len(list_defnodes):
                if list_defnodes[i]._id == cfgnode._id:
                    del list_defnodes[i]
                else:
                    i += 1

            list_usenodes += list_defnodes
            
            #print len(list_usenodes)
            for i in list_usenodes:
                if str(i).find("location")==-1:
                    list_usenodes.remove(i)
            loc_list=[]
            final_list=[]
            for i in list_usenodes:
                #print(i)
                if 'location:' in str(i):
                    #print(str(i))
                    location=str(i).split(",type:")[0].split("location:")[1][1:-1].split(":")
                    count=int(location[0])
                    loc_list.append(count)
            #print loc_list
            if len(loc_list)!=0:
                a=loc_list.index(max(loc_list))
                final_list.append(list_usenodes[a])
            for use_node in final_list:
                if use_node._id in _temp_list:
                    continue
                else:
                    _temp_list.append(use_node._id)

                if testID in _dict.keys():
                    _dict[testID].append(([str(use_node._id)], str(use_node.properties['functionId']), name))
                else:
                    _dict[testID] = [([str(use_node._id)], str(use_node.properties['functionId']), name)]

    return _dict


def get_all_array_use(db):
    _dict = {}
    list_arrays_node = get_arrays_node(db)
    for cfgnode in list_arrays_node:
        file_path = getFuncFile(db, int(cfgnode.properties['functionId']))
        testID = file_path.split('/')[-1]
        testID = '_'.join(testID.split('_')[:-1])
        array_defnode = get_def_node(db, cfgnode._id)
        _temp_list = []
        for node in array_defnode:
            name = node.properties['code'].strip()
            list_usenodes = get_all_use_bydefnode(db, node._id)
            list_defnodes = get_all_def_bydefnode(db, node._id)

            i = 0
            while i < len(list_defnodes):
                if list_defnodes[i]._id == cfgnode._id:
                    del list_defnodes[i]
                else:
                    i += 1

            list_usenodes += list_defnodes
			
            for use_node in list_usenodes:
                if use_node._id in _temp_list:
                    continue
                else:
                    _temp_list.append(use_node._id)

                if testID in _dict.keys():
                    _dict[testID].append(([str(use_node._id)], str(use_node.properties['functionId']), name))
                else:
                    _dict[testID] = [([str(use_node._id)], str(use_node.properties['functionId']), name)]

    return _dict


def get_all_integeroverflow_point(db):
    _dict = {}
    list_exprstmt_node = get_exprstmt_node(db)
    for node_id in list_exprstmt_node:
        query_str = "g.v(%d)" % node_id
        cfgnode = db.runGremlinQuery(query_str)

        if cfgnode.properties['code'].find(' = ') > -1:
            code = cfgnode.properties['code'].split(' = ')[-1]
            pattern = re.compile("((?:_|[A-Za-z])\w*(?:\s(?:\+|\-|\*|\/)\s(?:_|[A-Za-z])\w*)+)")                
            result = re.search(pattern, code)
       
            if result == None:
                continue
            else:
                file_path = getFuncFile(db, int(cfgnode.properties['functionId']))
                testID = file_path.split('/')[-1]
                testID = '_'.join(testID.split('_')[:-1])
                name = cfgnode.properties['code'].strip()

                if testID in _dict.keys():
                    _dict[testID].append(([str(cfgnode._id)], str(cfgnode.properties['functionId']), name))
                else:
                    _dict[testID] = [([str(cfgnode._id)], str(cfgnode.properties['functionId']), name)]

        else:
            code = cfgnode.properties['code']
            pattern = re.compile("(?:\s\/\s(?:_|[A-Za-z])\w*\s)")
            result = re.search(pattern, code)
            if result == None:
                continue

            else:
                file_path = getFuncFile(db, int(cfgnode.properties['functionId']))
                testID = file_path.split('/')[-1]
                testID = '_'.join(testID.split('_')[:-1])
                name = cfgnode.properties['code'].strip()

                if testID in _dict.keys():
                    _dict[testID].append(([str(cfgnode._id)], str(cfgnode.properties['functionId']), name))
                else:
                    _dict[testID] = [([str(cfgnode._id)], str(cfgnode.properties['functionId']), name)]

    return _dict


if __name__ == '__main__':
    j = JoernSteps()
    j.connectToDatabase()

    #NOTE: incrementally dumpt dictionary
    print 'sensifunc_slice_points'
#   _dict = get_all_sensitiveAPI(j)
    f = open("sensifunc_slice_points.pkl", 'wb')
    _dict = get_all_sensitiveAPI(j,f)
    pickle.dump(_dict, f, True)
    f.close()
#   print _dict

    #NOTE: all other functions ran fine
    sys.exit()

    print 'pointuse_slice_points'
    _dict = get_all_pointer_use(j)
    f = open("pointuse_slice_points.pkl", 'wb')
    pickle.dump(_dict, f, True)
    f.close()
#   print _dict

    print 'arraysuse_slice_points'
    _dict = get_all_array_use(j)
    f = open("arraysuse_slice_points.pkl", 'wb')
    pickle.dump(_dict, f, True)
    f.close()
#   print _dict

    print 'integeroverflow_slice_points'
    _dict = get_all_integeroverflow_point(j)
    f = open("integeroverflow_slice_points_new.pkl", 'wb')
    pickle.dump(_dict, f, True)
    f.close()
