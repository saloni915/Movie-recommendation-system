# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 18:30:01 2019

@author: Udit
"""
import sys


fp = open(sys.argv[1], "r")
if not fp:
    print('cannot open file')
    
filename=sys.argv[2]
count=0
i=0

wp = open(filename,"w")

while(True):
    ch=fp.read(1)
    if not ch:
        break
    if( ch == '@' or ch == '>'):
        continue
    if((ch == '\n') or (ch == '\t') or (ch == ' ')):
        count+=1
    else:
        wp.write(ch)
        i+=1
wp.close()

length=i
nt=[None]*length
cc=0
fp.seek(0,0)

while(True):
    ch=fp.read(1)
    if not ch:
        break
    if( ch == '@' or ch == '>'):
        cc = 10
        nt[cc]= ch 
    if((ch == '\n') or (ch == '\t') or (ch == ' ')):
        continue
    else:
        nt[cc] = ch
    print(ch)
    cc+=1
    
outfile=sys.argv[3]
wp1=open(outfile,"w")

for l in range(length):
    if(( (nt[l] == 'n') or (nt[l] == 'N') or (nt[l] == 'M') or (nt[l] == 'm') or  (nt[l] == 'k') or (nt[l] == 'K') or (nt[l] == 'w') or (nt[l] == 'W') or (nt[l] == 'S') or (nt[l] == 's'))):
        wp1.write(nt[l]+"\t0\n")
        
    if(((nt[l] == 'A') or (nt[l] == 'a') )):
        wp1.write(nt[l]+"\t-1\n")

    if(((nt[l] == 'T') or (nt[l] == 't'))):
        wp1.write(nt[l]+"\t1\n")
    
    if(((nt[l] == 'Y') or (nt[l] == 'y'))): #pYramidines(T,C)
        wp1.write(nt[l]+"\t1\n")
    
    if(((nt[l] == 'R') or (nt[l] == 'r'))): #puRines(A,G)
        wp1.write(nt[l]+"\t-1\n")
    
    if(((nt[l] == 'G') or (nt[l] == 'g'))):
       wp1.write(nt[l]+"\t-1\n")
       
    if(((nt[l] == 'C') or (nt[l] == 'c') )):
        wp1.write(nt[l]+"\t1\n")
    
  
