# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 20:57:59 2019

@author: vyas
"""

"""
Modelling:
    Define States:
        Threshold
        Trend = { Up, range-bound, Down }
            a {Trend == up } if {previous X min threshold has jumped}
              {}
        Each State is a tuple of 
          Sx = { Previous trend duration, Previous Day Trend, Current day Trend }
"""

import numpy as np
import csv
import codecs
from datetime import datetime

class RawDayData:
    def __init__(self, instr, o, h, l, c, v, time_of_day):
        self.instrument  = instr
        self.date = time_of_day[0]
        self.o = o
        self.h = h
        self.l = l
        self.c = c
        self.v = v
        self.TOD = time_of_day
    
    def GetCloseData(self):
        return self.TOD, o
    
    def GetEOD(self):
        return self.o[-1]

       

def ImportData(file_name):
    print(__name__)
    data=[]
    print("Importing data....")
    
    f=codecs.open(file_name,"rb",encoding="ascii")
    csvread=csv.reader(f,delimiter=',')
    for row in csvread:
        data.append(row)
    ndata = np.asarray(data)
    return data, ndata


def ParseInput(data):
    #instr = data[:,0]
    date = data[:,1]
    time = data[:,2]
    o = data[:,3]
    h = data[:,4]
    l = data[:,5]
    c = data[:,6]
    v = data[:,7]
    
    o = o.astype('float')
    h = h.astype('float')
    l = l.astype('float')
    c = c.astype('float')
    v = v.astype('int64')
 
    #
    # Convert date time
    count = len(time)
    tt = []
    for i in np.arange(count):
        s = date[i] +":" + time[i]
        dt = datetime.strptime(s, "%Y%m%d:%H:%M")
        tt = np.append(tt, dt)
        

    return tt, time, o, h, l, c, v

if __name__ == "__main__":
    file_name = "../Data/2019/01APR/ACC.txt"
    d,n = ImportData(file_name)
    dt,t,o,h,l,c,v = ParseInput(n)
    print(dt)
    