import glob
import numpy as np
import sys

ranks = glob.glob(str(sys.argv[1])+'/weights_*_'+str(sys.argv[2])+'.npy')

energy = 2
for rank in ranks:
    energy = energy + float(np.load(rank, allow_pickle=True)[0])
    
print(energy)