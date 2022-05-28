import os
import pickle

f = open("dict_cwe2father.pkl", 'rb')
d = pickle.load(f)
print(d.keys())
print(d['CWE-416'])
f.close()

print('===================')

#f = open("label_vec_type.pkl", 'rb')
f = open("label_vec_type_new.pkl", 'rb')
d = pickle.load(f)
print(d)
print('CWE-416' in d)
f.close()

print('===================')

#f = open("dict_testcase2code.pkl",'rb')
f = open("dict_testcase2code_new.pkl",'rb')
d = pickle.load(f)
for k,v in d.items():
    #if 'CWE191_Integer_Underflow__char_rand_multiply_12.c' in k:
    if 'CWE416_Use_After_Free__malloc_free_char_01' in k:
            print(k,v)
f.close()

print('===================')

#f = open("dict_flawline2filepath.pkl", 'rb')
f = open("dict_flawline2filepath_new.pkl", 'rb')
d = pickle.load(f)
for k,v in d.items():
    #if 'CWE416_Use_After_Free__malloc_free_long_16.c' in k:
    #if 'CWE191_Integer_Underflow__char_rand_multiply_12.c' in k:
    if 'CWE416_Use_After_Free__malloc_free_char_01' in k:
            print(k,v)
f.close()

print('===================')
