# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 09:19:42 2019

@author: vyasraj
version 1.1
"""
import numpy as np
import random as random

class QSAValue:
    def __init__ (self, name, alpha, gamma):
        self.name = name
        self.value = 0
        self.alpha = alpha
        self.gamma = gamma
            
    def UpdateValue(self, reward, qsaprime):
        '''
        Q(S,A) <- Q(S,A) + alpha*(reward, discount*(Q(send,A') - Q(S,A)))
        '''
        self.value = self.value + self.alpha*(reward + self.gamma*qsaprime - self.value )
        return
    
    def GetValue(self):
        return self.value

class Action:
    def __init__(self, state_name, action_name):
        self.action = action_name
        self.state = state_name
        self.action_name = state_name+action_name
        self.QSA = QSAValue(self.action_name, 0.1, 0.1) #FIXME hardcoding

    def compare (self, compare_val):
        if (self.action_name == compare_val):
            return True
        else:
            return False 
        
    def UpdateIndex(self, idx):
        self.idx = idx
    
    def GetStateAction(self):
        return self.action_name
    
    def GetIndex(self):
        return self.idx
    
    def GetActionType(self):
        return self.action
    
    def GetActionValue(self):
        return self.QSA.GetValue()
    
    def UpdateQValue(self, reward, qsaprime):
        self.QSA.UpdateValue(reward, qsaprime)

''' Stores all the valid states @ init time '''
class ActionMgr:
    def __init__(self, name):
        self.name = name
        self.valid_action = 0
        self.valid_action_list = []
        
    def CreateAction(self, state, action):
        action_name_str = state + action
        for i in np.arange(self.valid_action):
            a = self.valid_action_list[i]
            if (a.GetStateAction() == action_name_str):
                print("ERROR... print")
                return "already_present"
        
        new_action = Action(state, action)
        new_action.UpdateIndex(self.valid_action)
        self.valid_action +=1
        self.valid_action_list.append(new_action)

        return new_action

class State:
    def __init__(self, state):
        self.state = state
        self.valid_action_in_state = []
    
    def compare (self, compare_val):
        if (self.state == compare_val):
            return True
        else:
            return False
    
    def UpdateIndex(self, idx):
        self.idx = idx
    
    def GetState(self):
        return self.state
    
    def GetIndex(self):
        return self.idx
    
    ''' Stores a valid action list for this state '''
    def AddValidAction(self, action):
        self.valid_action_in_state.append(action)
        
    def GetFirstAction(self):
        self.getIndex = 0
        return True, self.valid_action_in_state[self.getIndex]
    
    def GetNextAction(self):
        self.getIndex += 1
        if self.getIndex < len(self.valid_action_in_state):
            return True, self.valid_action_in_state[self.getIndex]
        return False, 0

    def GetActionList(self):
        return self.valid_action_in_state 

    def GetMaxQAction(self):
        max_action = self.valid_action_in_state[0]
        max_value = max_action.GetActionValue()
        for i in np.arange(len(self.valid_action_in_state)):
            n = self.valid_action_in_state[i]
            n_value = n.GetActionValue()
            if (n_value > max_value):
                max_action = n
                max_value = n_value
        return max_action, max_value
    
    def GetSellAction(self):
        for i in np.arange(len(self.valid_action_in_state)):
            n = self.valid_action_in_state[i]
            if (n.GetActionType() ==  "Sell"):
                return n
        return "not found"


''' Stores all the valid states @ init time '''
class StateMgr:
    def __init__(self, name):
        self.name = name
        self.valid_states = 0
        self.valid_state_list = []
    
    def CreateStateSpace(self, state):
        for i in np.arange(self.valid_states):
            s = self.valid_state_list[i]
            if (s.GetState() == state):
                return "already_present"
        
        new_state = State(state)
        new_state.UpdateIndex(self.valid_states)
        self.valid_states +=1
        self.valid_state_list.append(new_state)
        return new_state
    
    def PrintStates(self):
        for i in np.arange(len(self.valid_state_list)):
            state = self.valid_state_list[i]
            print("idx: ", state.GetIndex(), " Name: ", state.GetState(), end = "")
            aindex = 0
            r, a = state.GetFirstAction()
            while(r==True):
                print(" Action#",aindex, ":(", a.GetActionType(), "", end = "")
                print (",", a.GetActionValue(), ")", end = "")
                r, a = state.GetNextAction() 
                aindex += 1
            print(" ")
            
    def GetState(self, state):
        for i in np.arange(self.valid_states):
            s = self.valid_state_list[i]
            if (s.GetState() == state):
                return s
        print(__name__, "Error.. did not find State", state)
        return "Not found"
    
    def GetFirst(self):
        self.getIndex = 0
        return True, self.valid_state_list[self.getIndex]
    
    def GetNext(self):
        self.getIndex += 1
        if self.getIndex < len(self.valid_state_list):
            return True, self.valid_state_list[self.getIndex]
        return False, 0

class Reward:
    def __init__(self, name, reward):
        self.name = name
        self.reward = reward
    
    def GetRewardVal(self):
        return self.reward
        
class Value:
    def __init__(self, name):
        self.value = name
        
    def compare (self, compare_val):
        if (self.value == compare_val):
            return True
        else:
            return False        

''' {S A R S} {S A R S} '''

class SARS:
    def __init__ (self, sbegin, action, reward, send):
        self.sbegin = sbegin
        self.action = action
        self.reward = reward
        self.send = send
    
    def GetBeginState(self):
        return self.sbegin
    
    def GetReward(self):
        return self.reward
    
    def GetAction(self):
        return self.action
    
    def GetSend(self):
        return self.send

    def StoreCookie(self, cookie):
        self.cookie = cookie
    
    def GetCookie(self):
        return self.cookie

class Episode:
    def __init__ (self, name):
        self.name = name
        self.sars_list = []
        self.last_Send = 0
        self.number_of_sars = 0
    
    def AddSars(self, sbegin, action, reward, send):
        sars = SARS(sbegin, action, reward, send)
        if (self.number_of_sars > 0):
            if (sbegin.GetState() != self.last_Send.GetState()):
                print(__name__, "SCREAM... error")
                return
        self.sars_list.append(sars)
        
        self.last_Send = send
        sars.StoreCookie(self.number_of_sars)
        self.number_of_sars += 1
        return
    
    def GetFirstSars(self):
        if (self.number_of_sars > 0):
            return True, self.sars_list[0]
        else:
            return False, ""
    
    def GetNext(self, sars): 
        return_next = False
        for i in np.arange(len(self.sars_list)):
            if (return_next == True):
                return True, self.sars_list[i]
            s = self.sars_list[i]
            if (s.GetCookie() == sars.GetCookie()):
                return_next = True
        return False, ""
    
    def ComputeQVal(self):
        for i in np.arange(len(self.sars_list)):
            sars = self.sars_list[i]
            max_action, max_value = sars.GetSend().GetMaxQAction()
            sars.GetAction().UpdateQValue(sars.GetReward(), max_value)

def SARSUT(state_mgr):
    day1 = ["U", "F", "D"]
    day2 = ["U", "F", "D"]
    hour1 = ["U", "F", "D"]
    hour2 = ["U", "F", "D"]
    day_state = "UU"

    """ generate random actions """
    position = "I"
    total_actions = 312
    new_state = day_state + hour1[0] + hour2[0] + position
    episode = Episode("test")

    for i in np.arange(total_actions):
        i1 = np.floor(len(hour1)*random.random())    
        i2 = np.floor(len(hour2)*random.random())    
        current_state = new_state
        s = state_mgr.GetState(current_state)
        alist = s.GetActionList()
        a1 = np.floor(len(alist)*random.random())
        print(a1, alist)
        action = alist[int(a1)]
        if (action.GetActionType() == "Buy"):
            position = "B"
            reward = 1
        elif (action.GetActionType() == "Sell"):
            position = "I"
            reward = 0
        elif (action.GetActionType() == "Idle"):
            position = position
            reward = 0
        else:
            print(__name__, "Error... ", action.GetActionType())
            exit(0)
        new_state = day_state + hour1[int(i1)] + hour2[int(i2)] + position
        n = state_mgr.GetState(new_state)
        episode.AddSars(s, action, reward, n)
        
    episode.ComputeQVal() 
    return episode

def UT():
    state_mgr = StateMgr("test")
    action_mgr = ActionMgr("test")
    day1 = ["U", "F", "D"]
    day2 = ["U", "F", "D"]
    hour1 = ["U", "F", "D"]
    hour2 = ["U", "F", "D"]
    Position = ["B", "I"]
    Action = ["Buy", "sell", "do_nothing"]
    for d1 in np.arange(len(day1)):
        for d2 in  np.arange(len(day2)):
            for h1 in np.arange(len(hour1)):
                for h2 in np.arange (len(hour2)):
                    str_val = day1[d1]+day2[d2]+hour1[h1]+hour2[h2] + "B"
                    s = state_mgr.CreateStateSpace(str_val)
                    ''' Valid actions at bought state '''
                    act_val = "Sell"
                    a = action_mgr.CreateAction(str_val, act_val)
                    s.AddValidAction(a)

                    act_val = "Idle"
                    a = action_mgr.CreateAction(str_val, act_val)
                    s.AddValidAction(a)
                    
                    ''' Valid action at I state '''
                    str_val = day1[d1]+day2[d2]+hour1[h1]+hour2[h2] + "I"
                    s = state_mgr.CreateStateSpace(str_val)
                    
                    act_val = "Buy"
                    a = action_mgr.CreateAction(str_val, act_val)
                    s.AddValidAction(a)

                    act_val = "Idle"
                    a = action_mgr.CreateAction(str_val, act_val)
                    s.AddValidAction(a)
                    
    SARSUT(state_mgr)
    state_mgr.PrintStates()

if ("__main__" == __name__):
    print("hello world")
    UT()
    
    