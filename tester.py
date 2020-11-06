import torch
import numpy as np
import sys
sys.path.insert(1,"./Models")
from ddqn import DDQN
from renderer import Render
from game import MineSweeper
import time

class Tester():
    def __init__(self,render_flag):
        self.model = DDQN(36,36)
        self.render_flag = render_flag
        self.width = 6
        self.height = 6
        self.env = MineSweeper(self.width,self.height,6)
        if(self.render_flag):
            self.renderer = Render(self.env.state)
        self.load_models(34000)
    
    def get_action(self,state):
        state = state.flatten()
        mask = (1-self.env.fog).flatten()
        action = self.model.act(state,mask)
        return action

    def load_models(self,number):
        path = "pre-trained\ddqn_dnn_gamma99.pth"
        dict = torch.load(path)
        self.model.load_state_dict(dict['current_state_dict'])
        self.model.epsilon = 0
    
    def do_step(self,action):
        i = int(action/self.width)
        j = action%self.width

        if(self.render_flag):
            self.renderer.state = self.env.state
            self.renderer.draw()
            self.renderer.bugfix()
        next_state,terminal,reward = self.env.choose(i,j)
        return next_state,terminal,reward
    

def win_tester():
    tester = Tester(False)
    state = tester.env.state
    mask = tester.env.fog
    games = 1000
    wins = 0
    i=0
    while(i<games):
        action = tester.get_action(state)
        next_state,terminal,reward = tester.do_step(action)
        state = next_state
        if(terminal):
            i+=1
            tester.env.reset()
            state = tester.env.state
            if(reward==1):
                wins+=1
    
    print(wins*100/games)


def slow_tester():

    tester = Tester(True)
    state = tester.env.state
    count = 0
    start = time.perf_counter()

    while(True):
        count+=1
        action = tester.get_action(state)
        next_state,terminal,reward = tester.do_step(action)
        state = next_state
        print(reward)
        time.sleep(1)

        if(terminal):
            if(reward==1):
                print("WIN")
            else:
                print("LOSS")
            tester.env.reset()
            state = tester.env.state
            break
        
        

def main():
    slow_tester()

main()
        
