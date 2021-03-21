#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random

class Tsetlin():
    def __init__(self, N, c1, c2):
        self.N = N
        self.c1 = c1
        self.c2 = c2
        self.c = [c1, c2]
        self.reward_count = [0, 0]
        self.action_count = [0, 0]
        self.ignore_first = 0
        
    def p1_inf(self):
        d1 = 1 - self.c1
        d2 = 1 - self.c2
        return 1.0/             ( 1 + (self.c1/self.c2)**self.N *                      ((self.c1-d1)/(self.c2-d2)) *                      ((self.c2**self.N-d2**self.N)/(self.c1**self.N-d1**self.N)))

    def next_state(self, state, beta):
        if beta == 0:
            if state != 1 and state != self.N+1:
                state = state - 1
        else:
            if state != self.N and state != 2*self.N:
                state = state + 1
            else:
                if state == self.N:
                    state = 2*self.N
                else:
                    state = self.N
        return state

    def reward(self, action):
        if random.uniform(0, 1) < self.c[action]:
            return 1
        else:
            return 0

    def action(self, state):
        if state <= self.N:
            return 0
        else:
            return 1

    def run(self, iterations, ignore_first, state):
        self.iterations = iterations
        self.ignore_first = ignore_first
        for n in range(0, iterations):
            alpha = self.action(state)
            beta = self.reward(alpha)
            state = self.next_state(state, beta)
            if n >= ignore_first:
                self.action_count[alpha] += 1
                if beta == 0:
                    self.reward_count[alpha] += 1
                
    def print_results(self):
        print('For the Tsetlin model')
        print('---------------------')
        print('N = {:d}, c1 = {:.3f}, c2 = {:.3f}'.format(self.N, self.c1, self.c2))
        print('for the final {:d} iterations:'.format(self.iterations - self.ignore_first))
        print('  rewards with action 1: {:d}, action 2: {:d}'.format(self.reward_count[0], self.reward_count[1]))
        print('  performed action 1 {:d} times, action 2 {:d} times'.format(self.action_count[0], self.action_count[1]))
        print('')

_N = 8
_state = _N
_iterations = 20000
_ignore_first = 1000
_c1 = 0.05
_c2 = 0.70
for i in range(0, 7):
    automaton = Tsetlin(_N, _c1 + i/10.0, _c2)
    automaton.run(_iterations, _ignore_first, _state)
    automaton.print_results()


# In[2]:


def binary_search(Nmin, Nmax, c1, c2, threshold):
    if Nmin == Nmax-1:
        automaton = Tsetlin(Nmin, c1, c2)
        if automaton.p1_inf() > threshold:
            return Nmin
        else:
            return Nmax
    automaton = Tsetlin(Nmin + (Nmax - Nmin)//2, c1, c2)
    if automaton.p1_inf() < threshold:
        return binary_search(Nmin + (Nmax - Nmin)//2, Nmax, c1, c2, threshold)
    else:
        return binary_search(Nmin, Nmax - (Nmax - Nmin)//2, c1, c2, threshold)

_threshold = 0.95  
_c2 = 0.70
for i in range (0, 7):
    _c1 = 0.05 + i/10.0
    if _c1 < 0.5:
        _Nmin = 1
        _Nmax = 2
        # find an Nmax that gives > 95% accuracy
        automaton = Tsetlin(_Nmax, _c1, _c2)
        while automaton.p1_inf() < _threshold:
            _Nmax *= 2
            automaton = Tsetlin(_Nmax, _c1, _c2)
        # now do a binary search to find the precise N required
        # for accuracy > 0.95
        print('c1 = {:.3f}, c2 = {:.3f}, for N = {:d}, p1(inf) >= {:.3f}'                  .format(_c1, _c2, binary_search(_Nmin, _Nmax, _c1, _c2, _threshold), _threshold))
    else:
        print(_c1, _c2, "no solution")
    
    


# In[3]:


limit = [2,2,3,5,9,100,400]
for i in range (0,7):
    _c1 = 0.05 + i/10.0
    automaton = Tsetlin(limit[i], _c1, _c2)
    automaton.run(20000, 1000, limit[i])
    automaton.print_results()


# In[142]:


import random

class Krylov():
    def __init__(self, N, c1, c2):
        self.N = N
        self.c1 = c1
        self.c2 = c2
        self.c = [c1, c2]
        self.reward_count = [0, 0]
        self.action_count = [0, 0]
        self.ignore_first = 0
        
    def next_state(self, state, beta):
        if beta == 0:
            # in this case it's identical to Tsetlin
            if state != 1 and state != self.N+1:
                state = state - 1
        else:
            if random.uniform(0, 1) < 0.5:
                if state !=1 and state != self.N+1:
                    state = state - 1
            else:
                if state == self.N:
                    state = 2*self.N
                elif state == 2*self.N:
                    state = self.N
                else:
                    state = state + 1
        return state

    def reward(self, action):         
        if random.uniform(0.0, 1.0) < self.c[action]:
            return 1
        else:
            return 0

    def action(self, state):
        if state <= self.N:
            return 0
        else:
            return 1

    def run(self, iterations, ignore_first, state):
        self.iterations = iterations
        self.ignore_first = ignore_first
        for n in range(0, iterations):
            alpha = self.action(state)
            beta = self.reward(alpha)
            state = self.next_state(state, beta)
            if n >= ignore_first:
                self.action_count[alpha] += 1
                if beta == 0:
                    self.reward_count[alpha] += 1
                
    def print_results(self):
        print('For the Krylov model')
        print('--------------------')
        print('N = {:d}, c1 = {:.3f}, c2 = {:.3f}'.format(self.N, self.c1, self.c2))
        print('for the final {:d} iterations:'.format(self.iterations - self.ignore_first))
        print('  rewards with action 1: {:d}, action 2: {:d}'.format(self.reward_count[0], self.reward_count[1]))
        print('  performed action 1 {:d} times, action 2 {:d} times'.format(self.action_count[0], self.action_count[1]))
        print('')


# In[148]:


_N = 4
_state = _N
_iterations = 20000
_ignore_first = 0
_c1 = 0.45
_c2 = 0.70
for i in range(0, 7):
    automaton = Krylov(_N, _c1, _c2)
    automaton.run(_iterations, _ignore_first, _state)
    automaton.print_results()
    automaton = Tsetlin(_N, _c1/2, _c2/2)
    automaton.run(_iterations, _ignore_first, _state)
    automaton.print_results()
    _N +=3
    print("*************")


# In[28]:


total = 0
for i in range(0,100):
    automaton = Tsetlin(4, 0.225, 0.35)
    automaton.run(20000, 19000, 4)
#    print(automaton.action_count[0])
#    automaton.print_results()
    total += automaton.action_count[0]


# In[24]:


automaton = Tsetlin(4, 0.225, 0.35)
print(automaton.p1_inf())


# In[20]:


for i in range(0,3):
    automaton = Krylov(4, 0.45, 0.7)
    automaton.run(20000, 19000, 4)
    automaton.print_results()


# In[29]:


print(total/100)


# In[154]:


automaton = Krylov(5, 0.45, 0.7)
automaton.run(20000, 0, 7)
automaton.print_results()


# In[214]:


import random

class L_RI():
    def __init__(self, N, c1, c2, lambda_r):
        self.N = N
        self.c1 = c1
        self.c2 = c2
        self.c = [c1, c2]
        self.reward_count = [0, 0]
        self.action_count = [0, 0]
        self.ignore_first = 0
        self.p1 = 0.5
        self.p2 = 0.5
        self.lambda_r = lambda_r
        
    def update_p_values(self, action, beta):
        if beta == 0:
            if action == 0:
                delta = self.lambda_r*self.p2
                self.p2 = self.p2 - delta
                self.p1 = self.p1 + delta
            else:
                delta = self.lambda_r*self.p1
                self.p1 = self.p1 - delta
                self.p2 = self.p2 + delta
        else:
            # no change when beta == 1
            pass

    def reward(self, action):         
        if random.uniform(0.0, 1.0) < self.c[action]:
            return 1
        else:
            return 0

    def action(self):
        if random.uniform(0.0, 1.0) < self.p1:
            return 0
        else:
            return 1

    def run(self, iterations, ignore_first):
        self.iterations = iterations
        self.ignore_first = ignore_first
        for n in range(0, iterations):
            alpha = self.action()
            beta = self.reward(alpha)
            self.update_p_values(alpha, beta)
            if n >= ignore_first:
                self.action_count[alpha] += 1
                if beta == 0:
                    self.reward_count[alpha] += 1
                
    def print_results(self):
        print('For the L_RI model')
        print('--------------------')
        print('N = {:d}, c1 = {:.3f}, c2 = {:.3f}'.format(self.N, self.c1, self.c2))
        print('for the final {:d} iterations:'.format(self.iterations - self.ignore_first))
        print('  rewards with action 1: {:d}, action 2: {:d}'.format(self.reward_count[0], self.reward_count[1]))
        print('  performed action 1 {:d} times, action 2 {:d} times'.format(self.action_count[0], self.action_count[1]))
        print('  performed action 1 {:.1f}%, action 2 {:.1f}%'              .format(self.action_count[0]*100.0/self.iterations, self.action_count[1]*100.0/self.iterations))
        print('  final p1: {:.4f} final p2: {:.4f}'.format(self.p1, self.p2))
        print('')


# In[220]:


automaton = L_RI(5, 0.45, 0.7, 0.3)
automaton.run(91, 0)
automaton.print_results()


# In[ ]:





# In[ ]:




