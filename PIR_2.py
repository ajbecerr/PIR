import pickle
import sys

with open(str(sys.argv[1])+'_'+str(sys.argv[2])+'_'+str(sys.argv[3])+'_'+str(sys.argv[4])+'.pkl', 'rb') as fp:
    person = pickle.load(fp)
    print('Loaded dictionary')
    print(person)
