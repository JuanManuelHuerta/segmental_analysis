import sys
import numpy as np
import scipy.spatial
import math



## Parameters
num_segs = 4


def distance(x1,x2,V):
    ##  This version uses the diagonal covariance matrix
    y = math.sqrt(np.sum(np.divide(np.square(x1-x2),V)))
    return y

def distance2(x1,x2,V):
    ## This version uses the full covariance matrix
    y = scipy.spatial.distance.mahalanobis(x1, x2, VI)
    return y

def find_medoid(R,V):
    if len(R)==1:
        return R[0]
    else:
        min_score=None
        min_index=None
        for i in range(len(R)):
            this_score=sum([distance2(R[i],R[j],V) for j in range(len(R))])
            if min_score is None:
                min_score = this_score
                min_index = i
            if min_score > this_score:
                min_score = this_score
                min_index = i                
        return [len(R), min_index, min_score, R[min_index].tolist()]

## Load one line of data into a 2D array

#fp=open("data/sample_01.txt","rt")
for line in sys.stdin:
    l_p = line.rstrip().split(" ",1)
    X=np.array([ [float(y) for y in x.split(",")] for x in eval(l_p[1])])
    V= np.var(X,0)
    # Split line into segments
    D=[]
    VI=np.linalg.inv(np.cov(X,rowvar=False))
    for i in range(len(X)-1):
        D.append(distance2(X[i],X[i+1],VI))
    S=np.sum(D)/(num_segs*0.9999)
    segment_membership= np.divide(np.cumsum(D),S).astype(int)
    # Find most representative vector set R
    R=[]
    working_sets=[[] for i in range(num_segs)]
    working_sets[0].append(X[0])
    for j in range(len(segment_membership)):
        working_sets[segment_membership[j]].append(X[j+1])
    for i in range(num_segs):
        R.append(find_medoid(working_sets[i],VI))
    print [(i, R[i]) for i in range(num_segs)]






