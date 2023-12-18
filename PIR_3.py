import numpy as np
import sys

def totalExpectation():
  II_II = np.load('II_'+str(sys.argv[1])+'_'+str(sys.argv[2])+'_'+str(sys.argv[3])+'_II.npy')
  HH_IZ = np.load('HH_'+str(sys.argv[1])+'_'+str(sys.argv[2])+'_'+str(sys.argv[3])+'_IZ.npy')
  HH_ZZ = np.load('HH_'+str(sys.argv[1])+'_'+str(sys.argv[2])+'_'+str(sys.argv[3])+'_ZZ.npy')
  val = 2*II_II[0] - HH_IZ[0] - HH_ZZ[0]
  return val

val = totalExpectation()
np.save(str(sys.argv[1])+'_'+str(sys.argv[2])+'_'+str(sys.argv[3])+'.npy', np.array([val, int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])]))
