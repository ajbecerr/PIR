import numpy as np
import pickle
import sys

def expectationVal(op_string, probs):
    val = 0
    if op_string == 'II':
        val = val + probs['00'] + probs['01'] + probs['10'] + probs['11']
    if op_string == 'IZ':
        val = val + probs['00'] - probs['01'] + probs['10'] - probs['11']
    if op_string == 'ZZ':
        val = val + probs['00'] - probs['01'] - probs['10'] + probs['11']
    return val

with open(str(sys.argv[1])+'_'+str(sys.argv[2])+'_'+str(sys.argv[3])+'_'+str(sys.argv[4])+'.pkl', 'rb') as fp:
    probs = pickle.load(fp)
    print('Loaded dictionary')
    print(probs)
    val = expectationVal(str(sys.argv[5]), probs)
    print(val)
    np.save(str(sys.argv[1])+'_'+str(sys.argv[2])+'_'+str(sys.argv[3])+'_'+str(sys.argv[4])+'_'+str(sys.argv[5])+'.npy', np.array([val, int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])]))
