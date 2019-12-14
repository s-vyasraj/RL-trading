# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 17:07:46 2019

@author: vyas
version 1.1
"""
import Training_input as ti
import matplotlib.pyplot as plt
import calendar
import numpy as np
import os.path
from os import path
import datetime
import RLAlgo as rl

class Trend:
    def __init__(self, instr):
        self.name = instr

class DataStore:
    def __init__(self, instr, year, month, day, number_of_days):
        self.name = instr
        self.data_list = []
        self.root_dir = "../Data/"
        self.start_year = year
        self.start_month = month
        self.start_day = day
        self.number_of_days = number_of_days
        
        self.current_year = self.start_year
        self.current_month = self.start_month
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


    def check_date(self, year, month, day):
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
                self.data_list.append(rd)
                self.count += 1
            else:
                print("No file exists: ", fname)
            
                   
            #Go to next day
            self.current_day += 1
            #print("Changing day..", self.current_day)
            if (self.check_date(self.current_year, self.current_month, self.current_day) == False):
                self.current_day = 1
                self.current_month += 1
                print("Changing month day ", self.current_month)
            
            if (self.check_date(self.current_year, self.current_month, self.current_day) == False):
                self.current_month = 1
                self.current_year +=1
                print("Changing year day ", self.current_year)

            if (self.check_date(self.current_year, self.current_month, self.current_day) == False):
                print("..bailing out..", self.current_year, self.current_month, self.current_day)   
                return
            d = datetime.datetime(year=self.current_year,month=self.current_month,day=self.current_day,hour=9)
            now = datetime.datetime.now()
            if (d > now):
                print("..Date is greater than today..", self.current_year, self.current_month, self.current_day)   
                return 
        return
    
    def GetFirst(self):
        self.get_index = 0
        data = self.data_list[self.get_index]
        self.get_index += 1
        return data
    
    def GetNext(self):
        data = self.data_list[self.get_index]
        self.get_index += 1
        return data
    
    def GetTotal(self):
        return self.count
    
    def GetName(self):
        return self.name
    
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


def CreateStatesActions(state_mgr, action_mgr):
    day1 = ["U", "F", "D"] #Up, Flat, Down
    day2 = ["U", "F", "D"] 
    day3 = ["U", "F", "D"]
    min15 = ["U", "F", "D"]
    hour1 = ["U", "F", "D"]
    Position = ["B", "I"]
    for d1 in np.arange(len(day1)):
        for d2 in  np.arange(len(day2)):
            for d3 in np.arange(len(day3)):
                for h1 in np.arange (len(min15)):
                    for h2 in np.arange(len(hour1)):
                        str_val = day1[d1]+day2[d2]+day3[d3]+ min15[h1]+ hour1[h2] + "B"
                        s = state_mgr.CreateStateSpace(str_val)
                        ''' Valid actions at bought state '''
                        act_val = "Sell"
                        a = action_mgr.CreateAction(str_val, act_val)
                        s.AddValidAction(a)

                        act_val = "Idle"
                        a = action_mgr.CreateAction(str_val, act_val)
                        s.AddValidAction(a)
                    
                        ''' Valid action at I state '''
                        str_val = day1[d1]+day2[d2]+day3[d3]+ min15[h1]+ hour1[h2] + "I"
                        s = state_mgr.CreateStateSpace(str_val)
                        
                        act_val = "Buy"
                        a = action_mgr.CreateAction(str_val, act_val)
                        s.AddValidAction(a)

                        act_val = "Idle"
                        a = action_mgr.CreateAction(str_val, act_val)
                        s.AddValidAction(a)

    return

class EpisodeMgr:                    
    def __init__(self, name, percentage, smgr, amgr):
        self.instr = name
        self.percentage_threshold = round(percentage, 4)
        self.smgr = smgr
        self.amgr = amgr
        self.buy = 0
        self.sell = 0
        self.total_gain = 0
        self.episode_number = 0
        self.episode_list = []
        self.episode_date = []
        self.episode_gain = []
        self.episode_total_gain = []
        self.live_gain = 0
    
    def Reset(self):
        self.buy = self.sell = 0
        self.total_gain = 0
        
    def GetState(self, o, c):
        val = o - c
        pctg = val/c*100
        pctg = round(pctg, 4)
        if (pctg > self.percentage_threshold):
            return "U" #UP
        elif (pctg < -1*self.percentage_threshold):
            return "D" # Down
        return "F"     #Flat

    def GetReward(self):
        gain = self.sell - self.buy
        gain = gain/self.buy*100
        gain = round(gain, 4)
        if (gain > self.percentage_threshold):
            return 2
        elif(gain > 0):
            return 1
        elif(gain <-1.0*self.percentage_threshold):
            return -5
        
        return 0
        
            
        
    def CreateEpisode(self, current_data, pday1, pday2, pday3):
        state_str = ""
        current_day_open = current_data.GetDayOpen()
        pday1_close = pday1.GetDayClose()
        pday2_close = pday2.GetDayClose()
        pday3_close = pday3.GetDayClose()
        
        state_str += self.GetState(current_day_open, pday1_close)
        state_str += self.GetState(current_day_open, pday2_close)
        state_str += self.GetState(current_day_open, pday3_close)
        
        tod, o = current_data.GetOpenData()
        #Walk through the day
        d15=datetime.timedelta(minutes=15)
        d60=datetime.timedelta(minutes=60)
        first_episode = True
        position = "I"
        episode = rl.Episode(instr)
        self.episode_list.append(episode)
        self.Reset()
        self.episode_date.append(tod[0])
        self.episode_total_gain.append(0)
        self.episode_number += 1
        
        for i in np.arange(len(o)):
            current_time = tod[i]
            d15lookup = current_time - d15
            d60lookup = current_time - d60
            if (d15lookup <= tod[0]):
                continue
            if (d60lookup <= tod[0]):
                continue
            for j in  np.arange(i):
                if (d60lookup > tod[j]):
                    d60idx = j
                    break
            for j in np.arange(i):
                if (d15lookup > tod[j]):
                    d15idx = j
                    break
            
            if (first_episode == False):
                previous_state_str = current_state_str
                previous_action = action
                previous_reward = reward
                
            current_state_str = state_str + self.GetState(o[i], o[d15idx])
            current_state_str += self.GetState(o[i], o[d60idx])
            current_state_str += position #no position
                
            
            s = self.smgr.GetState(current_state_str)
            action, max_value = s.GetMaxQAction()
            ## End of day check
            if (i > (len(o)-5)):
                if (position == "B"):
                    action = s.GetSellAction()
                    position = "I"
                    self.sell = o[i]
                    reward = self.GetReward()
                    self.total_gain += (self.sell - self.buy)
                else:
                    reward = 0
                    position = position
            elif (action.GetActionType() == "Buy"):
                position = "B"
                reward = 0
                self.buy = o[i]
            elif (action.GetActionType() == "Sell"):
                position = "I"
                self.sell = o[i]
                reward = self.GetReward()
                self.total_gain += (self.sell - self.buy)
            elif (action.GetActionType() == "Idle"):
                position = position
                reward = 0
            else:
                print(__name__, "Error... ", action.GetActionType())
                exit
                
            if (first_episode == True):
                # PRevious state exists
                first_episode = False
                print("...first episode: ", self.episode_number)
                continue
            else:
                prev_state = self.smgr.GetState(previous_state_str)
                episode.AddSars(prev_state, previous_action, previous_reward, s)
        
        episode.ComputeQVal()
        self.episode_gain.append(self.total_gain)
        return
    
    def RunLive(self, current_data, pday, pday2, pday3):
        self.CreateEpisode(current_data, pday, pday2, pday3)
        self.live_gain += self.total_gain
        self.episode_total_gain.append(self.live_gain)

        return
    
    def Show(self):
        x = np.arange(len(self.episode_total_gain))
        plt.plot(self.episode_total_gain)
        plt.title(self.instr)

        #plt.gcf().autofmt_xdate()
        plt.xlabel("Trade event")
        plt.ylabel("Cummulative normalized PnL")
        plt.grid()
        plt.show()
        return  

def PrintGraph(data_store):
    total_data = data_store.GetTotal()
    data = []
    previous_day = data_store.GetFirst()
    for k in np.arange(total_data-1):
        data.append(previous_day.GetDayClose())
        previous_day = data_store.GetNext() 
    
    plt.plot(data)
    plt.title(data_store.GetName())
    plt.xlabel('tick - close value')
    plt.ylabel('Price of Instrument')
    plt.grid()
    #plt.gcf().autofmt_xdate()

    plt.show()
    return          

def PrintCurrentDayGraph(data_store):
    total_data = data_store.GetTotal()
    data = []
    previous_day = data_store.GetFirst()
    for i in np.arange(189):
        previous_day = data_store.GetNext()
    tod, c = previous_day.GetCloseData()
    
    
    plt.plot(c)
    plt.title(data_store.GetName())
    plt.xlabel('Minute tick - close value')
    plt.ylabel('Price of Instrument')
    plt.grid()
    #plt.gcf().autofmt_xdate()

    plt.show()
    print("Variance:", np.var(c))
    print("Standard deviation:", np.std(c))
    print("Mean:", np.mean(c))
    
    
    return          
                
        
        
if __name__ == "__main__":
    instr = "BHEL"
    start_year = 2019
    start_month = 1
    start_day = 1
    instr_samples = 365
    percentage_threshold = 0.1 ###FIXME hardcoded value

    data_store = DataStore(instr, start_year, start_month, start_day, instr_samples)
    data_store.GetData()
    total_data = data_store.GetTotal()
    print("total number of entries: ", data_store.GetTotal())
    training_samples = int(total_data*0.7) - 4 ### Total of 70% of data is training stamples
    result_samples = int(total_data*0.3)
    
    state_mgr = rl.StateMgr(instr)
    action_mgr = rl.ActionMgr(instr)
    episode_mgr = EpisodeMgr(instr, percentage_threshold, state_mgr, action_mgr)
    CreateStatesActions(state_mgr, action_mgr)
    #PrintGraph(data_store)
    PrintCurrentDayGraph(data_store)

    
    #state_mgr.PrintStates()
 
    #
    # Generate Episodes
    for k in np.arange(2):
        prev_day3 = data_store.GetFirst()
        prev_day2 = data_store.GetNext()
        prev_day1 = data_store.GetNext()
        current_day = data_store.GetNext()
        for i in np.arange(training_samples):
            episode_mgr.CreateEpisode(current_day, prev_day1, prev_day2, prev_day3)
            prev_day3 = prev_day2
            prev_day2 = prev_day1
            prev_day1 = current_day
            current_day = data_store.GetNext()
    
    #
    # Measure performance for the next sets
    for i in np.arange(result_samples):
        episode_mgr.RunLive(current_day, prev_day1, prev_day2, prev_day3)
        prev_day3 = prev_day2
        prev_day2 = prev_day1
        prev_day1 = current_day
        current_day = data_store.GetNext()
    
    episode_mgr.Show()
    #state_mgr.PrintStates()
