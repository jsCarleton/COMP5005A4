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

print('Question 3 a)')
print("######################################################################################################")
class L_RI():
    def __init__(self, c1, c2, lambda_r):
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
                self.p1 = self.p1 + self.lambda_r*(1 - self.p1)
            else:
                self.p1 = (1 - self.lambda_r)*self.p1
            self.p2 = 1 - self.p1
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
                
    def run_until(self, threshold, ignore_first):
        self.iterations = 0
        self.ignore_first = ignore_first
        while self.p1 < threshold and self.p2 < threshold:
            alpha = self.action()
            beta = self.reward(alpha)
            self.update_p_values(alpha, beta)
            if self.iterations >= ignore_first:
                self.action_count[alpha] += 1
                if beta == 0:
                    self.reward_count[alpha] += 1
            self.iterations += 1

    def print_results(self):
        print('For the L_RI model')
        print('------------------')
        print('lambda_R = {:.3f}, c1 = {:.3f}, c2 = {:.3f}'.format(self.lambda_r, self.c1, self.c2))
        print('for the final {:d} iterations:'.format(self.iterations - self.ignore_first))
        print('  rewards with action 1: {:d}, action 2: {:d}'.format(self.reward_count[0], self.reward_count[1]))
        print('  performed action 1 {:d} times, action 2 {:d} times'.format(self.action_count[0], self.action_count[1]))
        print('  performed action 1 {:.1f}%, action 2 {:.1f}%'.format(self.action_count[0]*100.0/self.iterations, self.action_count[1]*100.0/self.iterations))
        print('  final p1: {:.4f} final p2: {:.4f}'.format(self.p1, self.p2))
        print('')

_lambda_r = 0.3
_iterations = 25
_ignore_first = 0
_c2 = 0.70
for i in range(0, 7):
    _c1 = 0.05 + i/10.0
    automaton = L_RI(_c1, _c2, _lambda_r)
    automaton.run_until(0.95, 0)
    automaton.print_results()
    
def binary_lsearch(lambda_min, lambda_max, c1, c2, threshold):
    # create and run the L_RI for the minimum lambda
    a1 = L_RI(c1, c2, lambda_min)
    a1.run_until(threshold, 0)
    # create and run the L_RI for the maximum lambda
    a2 = L_RI(c1, c2, lambda_max)
    a2.run_until(threshold, 0)
    # are we done searching?
    if lambda_max - lambda_min < 0.01:
        # yes, which one had fewer iterations
        if a1.iterations < a2.iterations:
            # the lower bound
            return lambda_min, a1.iterations
        else:
            # the upper bound
            return lambda_max, a2.iterations
    # the lambdas haven't converged yet
    # which one produced few iterations?
    if a1.iterations < a2.iterations:
        # the lower bound
        return binary_lsearch(lambda_min, lambda_max - (lambda_max - lambda_min)/2.0, c1, c2, threshold)
    else:
        # the upper bound
        return binary_lsearch(lambda_min + (lambda_max - lambda_min)/2.0, lambda_max, c1, c2, threshold)

_c2 = 0.70
_lambda_min = 0.1
_lambda_max = 0.9
_threshold = 0.99
for i in range(0, 7):
    lambdas = 0
    iters = 0
    _c1 = 0.05 + i/10.0
    for j in range(0, 10000):
        l, n = binary_lsearch(_lambda_min, _lambda_max, _c1, _c2, _threshold)
        lambdas += l
        iters += n
    print("L_RI optimal lambda_r is {:.3f} for c1={:.2f}, c2={:.2f} in {:d} iterations"\
              .format(lambdas/(j+1), _c1, _c2, iters//(j+1)))
              
count = [0,0]
its = 0
for i in range(0,1000):
    a = L_RI(0.65, 0.70, 0.86)
    a.run_until(0.98, 0)
    if a.p1 > a.p2:
        count[0] += 1
    else:
        count[1] += 1
    its += a.iterations
print(count[0], count[1], its/1000)
print("######################################################################################################")
