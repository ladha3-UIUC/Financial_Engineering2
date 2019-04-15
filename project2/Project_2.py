# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 06:51:32 2019

@author: 한승표
"""

#일단 상수로 놓고, payoff 코딩만 해보기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import copy
sigma = 0.25
r = 0.025
s0 = 195.09
Barrier = 0.78 * s0
cpn_rate = 0.020375
FV = 1000
lower = 0
q = 0.007
upper = 2*s0
jmax = 100
imax = 780 # mat - pricing date 
T = 1.25
pricing_date = dt.date(2019,3,21)
issue_date = dt.date(2019,3,26)
initial_ad = (issue_date-pricing_date).days / 365
review_date = [dt.date(2019,6,21),dt.date(2019,9,23),dt.date(2019,12,23),dt.date(2020,3,23),dt.date(2020,6,22)]
cpn_date = [dt.date(2019,6,26),dt.date(2019,9,26),dt.date(2019,12,27),dt.date(2020,3,26),dt.date(2020,6,25)]
ds = (upper-lower)/jmax
d_t = T/imax
s_range = np.linspace(lower,upper,jmax+1)
t_range = np.linspace(0,T,imax+1)
grid = np.array([np.linspace(lower,upper,jmax+1)]*imax)
grid = grid.T
barrier_node = int(Barrier/ds)
s0_node = int(s0/ds)
df = 1/(1+r*d_t)

#%%
i_cpn = []
for i in range(len(cpn_date)):
    i_cpn.append(int(((cpn_date[i]-issue_date).days/365)/d_t))

i_review = []
for i in range(len(review_date)):
    i_review.append(int((review_date[i]-issue_date).days/365 /d_t))

value_matrix=  np.zeros((jmax,imax+1))
#만기 때 페이오프
for i in range(jmax): 
    if s_range[i] >= s0 or s_range[i]>=Barrier:
        value_matrix[i,-1] = 1000*(1+cpn_rate)
#        
    elif s_range[i] < s0 and s_range[i]>Barrier:
        value_matrix[i,-1] = 1000*(cpn_rate+s_range[i]/s0)
        
    else:
        value_matrix[i,-1] = 1000*(1+(s_range[i]-s0)/s0)
        
#lower boundary
value_matrix[0,:]= 0
#upper boundary
indexing = 0
for i in range(imax):
    value_matrix[-1,i] = 1000*(1+cpn_rate) * np.exp(-(i_cpn[indexing] - i)*d_t)
    if i>= i_cpn[indexing]:
        indexing = indexing +1
#    while i >= i_cpn[indexing]:
#        if indexing == len(i_review)-1:break
#        indexing = indexing +1
#payoff
for i in np.arange(imax-1,-1,-1):
    for j in np.arange(1,jmax-1):
        exp_a = (0.5*(sigma**2)*(j**2)+0.5*(r-q)*j)*d_t
        exp_b = 1-r*d_t -(sigma**2)*(j**2)*d_t
        exp_c = (0.5*(sigma**2)*(j**2)-0.5*(r-q)*j)*d_t
        value_matrix[j,i] = exp_a * value_matrix[j+1,i+1] + exp_b*value_matrix[j,i+1]+ exp_c * value_matrix[j-1,i+1]
        
    if i in i_cpn:
        for k in range(1,jmax-1):
            if i ==88: pass
    
            if s_range[k] >= s0:
                value_matrix[k,i] = 1000 * (1+cpn_rate)

            if s_range[k]>Barrier and s_range[k]<s0:
                value_matrix[k,i] = 1000 * (cpn_rate) + value_matrix[k,i]

            
            else:
                value_matrix[k,i] = exp_a* value_matrix[k+1,i+1] + exp_b*value_matrix[k,i+1]+ exp_c * value_matrix[k-1,i+1]
        
#        if s_range[j] <Barrier:
#            value_matrix[j,i] = 1000*(1+(s_range[j]-s0)/s0)
            
#        if i in i_review:
#            if s_range[j] >=s0:
#                 value_matrix[j,i] = 1000 * (1+cpn_rate)
#            else:
#                 value_matrix[j,i] = exp_a* value_matrix[j+1,i+1] + exp_b*value_matrix[j,i+1]+exp_c* value_matrix[j-1,i+1]

print(value_matrix[50,0])

#%%
             
def TDMAsolver(a, b, c, d):
 
    nf = len(a)     # number of equations
    ac, bc, cc, dc = map(np.array, (a, b, c, d))     # copy the array
    for it in range(1, nf):
        mc = ac[it-1]/bc[it-1]
        bc[it] = bc[it] - mc*cc[it-1] 
        dc[it] = dc[it] - mc*dc[it-1]

    xc = bc
    xc[-1] = dc[-1]/bc[-1]

    for il in range(nf-2, -1, -1):
        xc[il] = (dc[il]-cc[il]*xc[il+1])/bc[il]

#    del bc, cc, dc  # delete variables from memory

    return xc  
#%%
value_matrix_ = np.zeros((jmax,imax+1))

for i in range(jmax): 
    if s_range[i] >= s0 or s_range[i]>=Barrier:
        value_matrix_[i,-1] = 1000*(1+cpn_rate)
#        
    elif s_range[i] < s0 and s_range[i]>Barrier:
        value_matrix_[i,-1] = 1000*(cpn_rate+s_range[i]/s0)
    elif s_range[i]<s0 and s_range[i] <Barrier:
        value_matrix_[i,-1] = 1000*(1+(s_range[i]-s0)/s0)

#lower boundary
value_matrix_[0,:]= 0
#upper boundary
indexing = 0
for i in range(imax):
    value_matrix_[-1,i] = 1000*(1+cpn_rate) * np.exp(-(i_cpn[indexing] - i)*d_t)
    if i>= i_cpn[indexing]:
        indexing = indexing +1
        
value_matrix__ =value_matrix_.copy()

for i in np.arange(imax-1,-1,-1):
    a_matrix = np.zeros(jmax);b_matrix = np.zeros(jmax);c_matrix = np.zeros(jmax);d_matrix = np.zeros(jmax)
    d_matrix[0] = 0; d_matrix[-1] =  1000*(1+cpn_rate)
    b_matrix[0] = 1 ;c_matrix[0]=0 ; a_matrix[-1]=0 ;b_matrix[-1]=1
    
    for j in np.arange(1,jmax-1):
        a_matrix[j] = 0.25*((sigma**2)*(j**2)-(r-q)*j)
        b_matrix[j] = -0.5*((sigma**2)*(j**2)+r+2/d_t)
        c_matrix[j] = 0.25*((sigma**2)*(j**2)+(r-q)*j)
        d_matrix[j] = -0.25*((sigma**2)*(j**2)-(r-q)*j)*value_matrix_[j-1,i+1] \
                +0.5*((sigma**2)*(j**2)+r-(2/d_t))*value_matrix_[j,i+1] \
                -0.25*((sigma**2)*(j**2)+(r-q)*j)*value_matrix_[j+1,i+1]

    x = np.matrix(np.diag(b_matrix)+np.diag(a_matrix[1:],k=-1)+np.diag(c_matrix[:-1],k=1))
    value_matrix_[:,i] = np.linalg.solve(x,d_matrix)
    value_matrix__[:,i] = TDMAsolver(a_matrix[1:],b_matrix,c_matrix[:-1],d_matrix)
    if i in i_cpn:
        for k in np.arange(1,jmax-1):
                if i ==93: 
                    if s_range[k] >Barrier and s_range[k] <s0:
                        value_matrix[k,93] = 1000 * (cpn_rate) + value_matrix_[k,93]
                        value_matrix__[k,93] = 1000 * (cpn_rate) + value_matrix_[k,93]
                else:   
                    if s_range[k] >= s0:
                        value_matrix[k,i] = 1000 * (1+cpn_rate)
                        value_matrix__[k,i] = 1000 * (1+cpn_rate)
                        
                    elif s_range[k]>=Barrier and s_range[k]<s0:
                        value_matrix[k,i] = 1000 * (cpn_rate) + value_matrix_[k,i]
                        value_matrix__[k,i] = 1000 * (cpn_rate) + value_matrix_[k,i]
                    elif s_range[k] < Barrier:
                        value_matrix_[k,i]=value_matrix_[k,i]
                        value_matrix__[k,i]=value_matrix_[k,i]
print(value_matrix_[50,0])
print(value_matrix__[50,0])