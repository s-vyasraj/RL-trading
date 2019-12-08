# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 20:06:44 2019

@author: vyas

Policy:   
    
States:
    {n-day Previous Trend} x {Bought, no-position}
     n=4
     day trend = up { > 1%}
           = down { < -1%}
           = flat { [-1%, 1%] }
     
Starting State: {no-position, n-day-trend}

Actions:
    {Buy, Sell, hold}

Termination State: 
     { 
       T1: Gain of 15%,
       T2: Portfolio risk is < -25% drop
       T3: 6th-hour with gain
       T4: 6th-hour with loss
      }
     
Reward Structure: 
     -  0 for all States
     - +5 for reaching Termination State T1
     - -1 for reaching Termination State T2
     - +1/4 for reaching Temination State  T3
     - -1/2 for reaching Termination State T4

"""

class Policy:
    

    

class EnvStates:
    def __init__(self, name, number_of_previous_days, day_threshold):
        self.name = name
        self.number_of_prev_days = number_of_previous_days
        self.day_threshold = day_threshold
        self.instrument_trend = []
        self.instrument_days = []
        self.instrument_day_entries = 0

    def UpdateDayTrend(self, date, open_value, close_value):
        self.instrument_days.append(date)
        self.instrument_day_entries += 1
        diff = close_value - open_value
        pctg = diff/open_value*100
        if (pctg > self.day_threshold):
            self.instrument_trend.append("U")
        elif (pctg < -1.0*(self.day_threshold)):
            self.instrment_trend.append("D")
        else:
            self.instrument_trend.append("F")
        
    def GetCurrentEnvState(self):
        if (self.instrument_day_entries < self.number_of_prev_days):
            return "invalid"
        
        state_str = ""
        values = self.instrument_trend[-self.number_of_prev_days:]
        for i in np.arange(len(values)):
            idx = self.number_of_prev_days-1-i
            state_str += values[idx]
        
        return state_str
        
        


class Reward:
    def __init__(self, name, env_state):
        self.name = name
        self.env_state = env
    
    def GetReward(action,  ): 