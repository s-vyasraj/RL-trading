# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 17:07:46 2019

@author: vyas
"""
import Training_input as ti
import matplotlib.pyplot as plt
import calendar
import numpy as np
import os.path
from os import path

class DataStore:
    def __init__(self, instr, year, month, day, number_of_days):
        self.name = instr
        self.data_list = []
        self.root_dir = "../Data"
        self.start_year = year
        self.start_month = month
        self.start_day = day
        self.number_of_days = number_of_days
        
        self.current_year = self.start_year
        self.current_month = self.current_month
        self.current_day = self.start_day
        self.count = 0
        
    def DoesFileExist(self, year, month, day):
        data_dir = self.root_dir
        d = str(day).zfill(2)
        m = calendar.month_abbr[month]
        m.upper()
        file_name = data_dir + str(year) + "/" +  str(d) + m + "/" + self.name + ".txt"
        if (path.exists(file_name) == True):
            return True, file_name
        else:
            return False, file_name        


    def check_date(year, month, day):
        correctDate = None
        try:
            newDate = datetime.datetime(year, month, day)
            correctDate = True
        except ValueError:
            correctDate = False
        
        return correctDate

    def GetData(self):
        while(self.count < self.number_of_days):
            res, fname = self.DoesFileExist(self.current_year, self.current_month, self.current_day)
            if (res == True):
                d1,n1 = ti.ImportData(fname)
                d, t, o, h , l , c, v = ti.ParseInput(n1)
                rd = ti.RawDayData(self.name, o, h, l, c, v, d)
                data_list.append(rd)
                self.count += 1
            
            #Go to next day
            self.current_day += 1
            if (self.check_date(self.current_year, self.current_month, self.current_day) == False):
                self.current_day = 1
                self.current_month += 1
            
            if (self.check_date(self.current_year, self.current_month, self.current_day) == False):
                self.current_month = 1
                self.current_year +=1

            if (self.check_date(self.current_year, self.current_month, self.current_day) == False):
                print("..bailing out..", self.current_year, self.current_month, self.current_day)   
                return
            d = datetime.datetime(year=self.current_year,month=self.current_month,day=self.current_day,hour=9)
            now = datetime.datetime.now()
            if (d > now):
                print("..Date is greater than today..", self.current_year, self.current_month, self.current_day)   
                return 
        return
    
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
    