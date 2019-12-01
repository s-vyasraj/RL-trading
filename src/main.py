# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 17:07:46 2019

@author: vyas
"""
import Training_input as ti
import matplotlib.pyplot as plt
import calendar
import numpy as np

def Show(time, y1, y2):
    x = np.arange(len(time))
    plt.plot(x,y1)
    plt.gcf().autofmt_xdate()

    plt.show()
    return

def GetTrainingDataFile(year, month, day, instr):
    data_dir = "../Data/"
    d = str(day).zfill(2)
    m = calendar.month_abbr[month]
    m.upper()
    file_name = data_dir + str(year) + "/" +  str(d) + m + "/" + instr + ".txt"
    return file_name
    
    
if __name__ == "__main__":
    #file_name = "../Data/2019/01APR/ACC.txt"
    file_name = GetTrainingDataFile(2019,5,13,"ACC")
    print(file_name)
    d1,n1 = ti.ImportData(file_name)
    d, t, o, h , l , c, v = ti.ParseInput(n1)
    
    print(c)
    Show(t,c,v)
    