import random

######################## Assignment 4 Question 1 ########################
# A class to implement a two action Tsetlin automaton
# Constructor arguments are:
# N - the depth of the automaton
# c1, c2 - the penalty probabilities for each action
class Tsetlin():
    # Constructor
    # Additional state, beyond the constructor parameters, for this object:
    # c - an array with the penalty probabilities (for convenience)
    # iterations - number of times the model was run 
    # reward_count - number of times a given action was rewarded
    # action_count - number of times a given action was performed
    # ignore_first - numer of iterations to ignore for counting purposes
    def __init__(self, N, c1, c2):
        self.N = N
        self.c1 = c1
        self.c2 = c2
        self.c = [c1, c2]
        self.iterations = 0
        self.reward_count = [0, 0]
        self.action_count = [0, 0]
        self.ignore_first = 0
 
    # next_state function
    # given:
    # state - current state
    # beta - action outcome, 0 for reward, 1 for penalty
    # return:
    # new state       
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

    # reward function
    # given:
    # action - 0 for action 1, 1 for action 2
    # return:
    # the reward determined by the action and the penalty probabilities
    def reward(self, action):
        if random.uniform(0, 1) < self.c[action]:
            return 1
        else:
            return 0

    # action function
    # given:
    # state - the current state
    # return:
    # the action to be taken
    def action(self, state):
        if state <= self.N:
            return 0
        else:
            return 1
    # run the automaton
    # given:
    # iterations - number of times to run the automaton
    # ignore_first - the number of runs to ignore for reporting purposes
    # state - initial state of the automaton
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
     
    # print the results of running the automaton           
    def print_results(self):
        print('For the Tsetlin model')
        print('---------------------')
        print('N = {:d}, c1 = {:.3f}, c2 = {:.3f}'.format(self.N, self.c1, self.c2))
        print('for the final {:d} iterations:'.format(self.iterations - self.ignore_first))
        print('  rewards with action 1: {:d}, action 2: {:d}'.format(self.reward_count[0], self.reward_count[1]))
        print('  performed action 1 {:d} times, action 2 {:d} times'.format(self.action_count[0], self.action_count[1]))
        print('  performed action 1 {:.1f}%, action 2 {:.1f}%'.format(self.action_count[0]*100.0/self.iterations, self.action_count[1]*100.0/self.iterations))
        print('')

print("Question 1 a)")
print("######################################################################################################")
_N = 4
_iterations = 20000
_ignore_first = 0
_c1 = 0.05
_c2 = 0.70
for i in range(0, 7):
    automaton = Tsetlin(_N, _c1 + i/10.0, _c2)
    automaton.run(_iterations, _ignore_first, int(1 + random.uniform(0.0, 1.0)*2*_N))
    automaton.print_results()
print("######################################################################################################")

def p1_inf(N, c1, c2):
    d1 = 1 - c1
    d2 = 1 - c2
    return 1.0/( 1 + (c1/c2)**N *((c1-d1)/(c2-d2))\
        * ((c2**N-d2**N)/(c1**N-d1**N)))

def binary_search(Nmin, Nmax, c1, c2, threshold):
    if Nmin == Nmax-1:
        if p1_inf(Nmin, c1, c2) > threshold:
            return Nmin
        else:
            return Nmax
    if p1_inf(Nmin + (Nmax - Nmin)//2, c1, c2) < threshold:
        return binary_search(Nmin + (Nmax - Nmin)//2, Nmax, c1, c2, threshold)
    else:
        return binary_search(Nmin, Nmax - (Nmax - Nmin)//2, c1, c2, threshold)

print('Question 1 b)')
print("######################################################################################################")
_threshold = 0.95  
_c2 = 0.70
for i in range (0, 7):
    _c1 = 0.05 + i/10.0
    if _c1 < 0.5:
        _Nmin = 1
        _Nmax = 2
        # find an Nmax that gives > 95% accuracy
        while p1_inf(_Nmax, _c1, _c2) < _threshold:
            _Nmax *= 2
        # now do a binary search to find the precise N required
        # for accuracy > 0.95
        _N =  binary_search(_Nmin, _Nmax, _c1, _c2, _threshold)
        print('c1 = {:.3f}, c2 = {:.3f}, for N = {:d}, p1(inf) = {:.3f}'\
            .format(_c1, _c2, _N, p1_inf(_N, _c1, _c2)))
    else:
        print(_c1, _c2, "no solution")
print("######################################################################################################")

print('Question 1 c)')
print("######################################################################################################")
limit = [2,2,3,5,9,100,400]
for i in range (0,7):
    _c1 = 0.05 + i/10.0
    automaton = Tsetlin(limit[i], _c1, _c2)
    automaton.run(20000, 0, limit[i])
    automaton.print_results()
print('c1 = {:.3f}, c2 = {:.3f}, for N = {:d}, p1(inf) = {:.3f}'\
    .format(0.55, 0.70, 100, p1_inf(100, 0.55, 0.70)))
print('c1 = {:.3f}, c2 = {:.3f}, for N = {:d}, p1(inf) = {:.3f}'\
    .format(0.65, 0.70, 400, p1_inf(400, 0.65, 0.70)))
print("######################################################################################################")

print('Question 2')
print("######################################################################################################")
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
        print('  performed action 1 {:.1f}%, action 2 {:.1f}%'.format(self.action_count[0]*100.0/self.iterations, self.action_count[1]*100.0/self.iterations))
        print('')

_N = 4
_state = _N
_iterations = 20000
_ignore_first = 0
_c2 = 0.70
for i in range(0, 7):
    _c1 = 0.05 + i/10.0
    automaton = Krylov(_N, _c1, _c2)
    automaton.run(_iterations, _ignore_first, _state)
    automaton.print_results()
    automaton = Tsetlin(_N, _c1/2, _c2/2)
    automaton.run(_iterations, _ignore_first, _state)
    automaton.print_results()
    print("*************")
print("######################################################################################################")

total = 0
for i in range(0,100):
    automaton = Tsetlin(4, 0.225, 0.35)
    automaton.run(20000, 19000, 4)
    total += automaton.action_count[0]

automaton = Tsetlin(4, 0.225, 0.35)
print(p1_inf(4, 0.225, 0.35))


for i in range(0,3):
    automaton = Krylov(4, 0.45, 0.7)
    automaton.run(20000, 19000, 4)
    automaton.print_results()

print(total/100)

automaton = Krylov(5, 0.45, 0.7)
automaton.run(20000, 0, 7)
automaton.print_results()

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
        print('  performed action 1 {:.1f}%, action 2 {:.1f}%'.format(self.action_count[0]*100.0/self.iterations, self.action_count[1]*100.0/self.iterations))
        print('  final p1: {:.4f} final p2: {:.4f}'.format(self.p1, self.p2))
        print('')

automaton = L_RI(5, 0.45, 0.7, 0.3)
automaton.run(91, 0)
automaton.print_results()